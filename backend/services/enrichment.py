import asyncio
import logging

import httpx

from core.config import get_settings
from models.schemas import Song

logger = logging.getLogger(__name__)

ITUNES_SEARCH_URL = "https://itunes.apple.com/search"
LOOKUP_TIMEOUT = 5.0
MAX_CONCURRENT_LOOKUPS = 5
MAX_CACHE_ENTRIES = 500

_semaphore = asyncio.Semaphore(MAX_CONCURRENT_LOOKUPS)
_cache: dict[str, dict] = {}


async def enrich(songs: list[Song]) -> list[Song]:
    """Fill preview_url/artwork_url/store_url from the iTunes catalog. Never
    raises: a lookup failure just leaves those three fields null."""
    if not get_settings().ENABLE_ENRICHMENT:
        return songs

    try:
        async with httpx.AsyncClient(timeout=LOOKUP_TIMEOUT) as client:
            results = await asyncio.gather(
                *(_enrich_one(client, song) for song in songs),
                return_exceptions=True,
            )
    except Exception:
        logger.warning("Enrichment step failed outright; returning songs unenriched")
        return songs

    return [
        song if isinstance(result, BaseException) else result
        for song, result in zip(songs, results)
    ]


async def _enrich_one(client: httpx.AsyncClient, song: Song) -> Song:
    cache_key = f"{song.artist}|{song.title}".lower()
    if cache_key in _cache:
        return song.model_copy(update=_cache[cache_key])

    async with _semaphore:
        try:
            response = await client.get(
                ITUNES_SEARCH_URL,
                params={"term": f"{song.artist} {song.title}", "entity": "song", "limit": 1},
            )
            response.raise_for_status()
            results = response.json().get("results", [])
        except Exception:
            logger.warning("iTunes lookup failed for %r", cache_key)
            return song

    if not results:
        return song

    match = results[0]
    fields = {
        "preview_url": match.get("previewUrl"),
        "artwork_url": (match.get("artworkUrl100") or "").replace("100x100", "300x300") or None,
        "store_url": match.get("trackViewUrl"),
    }

    if len(_cache) < MAX_CACHE_ENTRIES:
        _cache[cache_key] = fields

    return song.model_copy(update=fields)
