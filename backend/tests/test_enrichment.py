import httpx
import pytest

from core.config import get_settings
from models.schemas import Song
from services import enrichment


@pytest.fixture(autouse=True)
def _enable_enrichment(monkeypatch):
    monkeypatch.setenv("ENABLE_ENRICHMENT", "true")
    get_settings.cache_clear()
    enrichment._cache.clear()
    yield
    enrichment._cache.clear()


class FakeResponse:
    def __init__(self, payload: dict, status_code: int = 200):
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            request = httpx.Request("GET", "https://itunes.apple.com/search")
            raise httpx.HTTPStatusError("error", request=request, response=self)

    def json(self):
        return self._payload


async def test_normal_match_maps_and_upsizes_artwork(monkeypatch):
    async def fake_get(self, url, params=None):
        return FakeResponse({
            "results": [{
                "previewUrl": "https://example.com/preview.m4a",
                "artworkUrl100": "https://example.com/art/100x100bb.jpg",
                "trackViewUrl": "https://music.apple.com/track/1",
            }]
        })

    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get)

    [enriched] = await enrichment.enrich([Song(title="Time", artist="Pink Floyd")])

    assert enriched.preview_url == "https://example.com/preview.m4a"
    assert enriched.artwork_url == "https://example.com/art/300x300bb.jpg"
    assert enriched.store_url == "https://music.apple.com/track/1"


async def test_empty_results_leaves_fields_null(monkeypatch):
    async def fake_get(self, url, params=None):
        return FakeResponse({"results": []})

    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get)

    [enriched] = await enrichment.enrich([Song(title="Nonexistent", artist="Nobody")])

    assert enriched.preview_url is None
    assert enriched.artwork_url is None
    assert enriched.store_url is None


async def test_timeout_leaves_fields_null_and_does_not_raise(monkeypatch):
    async def fake_get(self, url, params=None):
        raise httpx.TimeoutException("timed out")

    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get)

    [enriched] = await enrichment.enrich([Song(title="Time", artist="Pink Floyd")])

    assert enriched.preview_url is None
    assert enriched.artwork_url is None
    assert enriched.store_url is None
