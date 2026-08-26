import json

import pytest

from core.constants import PLAYLIST_SIZE
from services.playlist_service import _parse_songs, generate_playlist

_FIVE_SONGS = [{"title": f"Song {i}", "artist": f"Artist {i}"} for i in range(PLAYLIST_SIZE)]
_CLEAN_JSON = json.dumps({"songs": _FIVE_SONGS})


class FakeProvider:
    def __init__(self, text: str):
        self._text = text

    async def generate(self, prompt: str) -> str:
        return self._text


def test_clean_json():
    assert _parse_songs(_CLEAN_JSON) == _FIVE_SONGS


def test_json_wrapped_in_fences():
    fenced = f"```json\n{_CLEAN_JSON}\n```"
    assert _parse_songs(fenced) == _FIVE_SONGS


def test_json_with_prose_preamble():
    prose = f"Sure, here is your playlist:\n{_CLEAN_JSON}\nEnjoy!"
    assert _parse_songs(prose) == _FIVE_SONGS


def test_malformed_json_raises():
    with pytest.raises(json.JSONDecodeError):
        _parse_songs("{not valid json")


async def test_malformed_response_falls_back():
    provider = FakeProvider("{not valid json")
    result = await generate_playlist("Rock", provider)
    assert result.source == "fallback"
    assert len(result.songs) == PLAYLIST_SIZE


async def test_wrong_song_count_falls_back():
    three_songs = json.dumps({"songs": _FIVE_SONGS[:3]})
    provider = FakeProvider(three_songs)
    result = await generate_playlist("Rock", provider)
    assert result.source == "fallback"
    assert len(result.songs) == PLAYLIST_SIZE
