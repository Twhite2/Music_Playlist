from typing import Literal

from pydantic import BaseModel, Field

from core.constants import GENRES

Genre = Literal[tuple(GENRES)]


class PlaylistRequest(BaseModel):
    genre: Genre


class Song(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    artist: str = Field(min_length=1, max_length=200)
    preview_url: str | None = None
    artwork_url: str | None = None
    store_url: str | None = None


class PlaylistResponse(BaseModel):
    genre: Genre
    source: Literal["model", "fallback"]
    songs: list[Song]
