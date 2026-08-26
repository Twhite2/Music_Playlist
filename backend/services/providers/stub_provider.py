import json

from core.constants import PLAYLIST_SIZE

_STUB_SONGS = [
    {"title": f"Stub Track {i}", "artist": f"Stub Artist {i}"} for i in range(1, PLAYLIST_SIZE + 1)
]


class StubProvider:
    """Offline TextGenerator: returns a fixed, valid JSON payload with no
    network access, so the pipeline is testable and demoable offline."""

    async def generate(self, prompt: str) -> str:
        return json.dumps({"songs": _STUB_SONGS})
