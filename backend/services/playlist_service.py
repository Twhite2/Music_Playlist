import json
import logging
import re

from pydantic import ValidationError

from core.constants import FALLBACK_PLAYLISTS, PLAYLIST_SIZE
from models.schemas import Song, PlaylistResponse
from services.enrichment import enrich
from services.prompts import build_playlist_prompt
from services.providers.base import ProviderUnavailableError, TextGenerator

logger = logging.getLogger(__name__)

_FENCE_RE = re.compile(r"^```[a-zA-Z]*\n?|```$")


async def generate_playlist(genre: str, provider: TextGenerator) -> PlaylistResponse:
    prompt = build_playlist_prompt(genre)

    songs = await _try_generate(provider, prompt)
    if songs is None:
        songs = await _try_generate(provider, prompt)

    if songs is not None:
        return PlaylistResponse(genre=genre, source="model", songs=await enrich(songs))

    fallback_data = FALLBACK_PLAYLISTS.get(genre)
    if fallback_data is None:
        raise ProviderUnavailableError(f"No fallback playlist available for genre {genre!r}")

    fallback_songs = [Song(**item) for item in fallback_data]
    return PlaylistResponse(genre=genre, source="fallback", songs=await enrich(fallback_songs))


async def _try_generate(provider: TextGenerator, prompt: str) -> list[Song] | None:
    try:
        raw = await provider.generate(prompt)
    except ProviderUnavailableError as exc:
        logger.warning("Provider call failed: %s", exc)
        return None

    try:
        songs_data = _parse_songs(raw)
    except (json.JSONDecodeError, ValueError):
        logger.warning("Could not parse provider response as JSON: %r", raw[:200])
        return None

    songs = _to_validated_songs(songs_data)
    if songs is None:
        logger.warning("Provider response did not contain %d valid songs: %r", PLAYLIST_SIZE, raw[:200])
    return songs


def _parse_songs(text: str) -> list:
    """Strip whitespace/code fences and, if the JSON is buried in prose,
    extract the outer object or array before decoding. The prompt asks for
    an object (``{"songs": [...]}``) since OpenAI's JSON mode requires an
    object at the top level, but this also accepts a bare array so a model
    that ignores the shape instruction still parses instead of falling
    back unnecessarily."""
    cleaned = _FENCE_RE.sub("", text.strip()).strip()

    if cleaned and cleaned[0] not in "{[":
        starts = [i for i in (cleaned.find("{"), cleaned.find("[")) if i != -1]
        if starts:
            start = min(starts)
            end = cleaned.rfind("}" if cleaned[start] == "{" else "]")
            if end != -1:
                cleaned = cleaned[start:end + 1]

    parsed = json.loads(cleaned)
    songs_data = parsed.get("songs") if isinstance(parsed, dict) else parsed
    if not isinstance(songs_data, list):
        raise ValueError("Response JSON did not contain a songs array")
    return songs_data


def _to_validated_songs(songs_data: list) -> list[Song] | None:
    if len(songs_data) != PLAYLIST_SIZE:
        return None
    try:
        return [Song(title=item.get("title", ""), artist=item.get("artist", "")) for item in songs_data]
    except (AttributeError, ValidationError):
        return None
