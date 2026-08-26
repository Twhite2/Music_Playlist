from fastapi import APIRouter, HTTPException, Request

from models.schemas import PlaylistRequest, PlaylistResponse
from services import playlist_service
from services.providers.base import ProviderUnavailableError

router = APIRouter()


@router.post("/playlist", response_model=PlaylistResponse)
async def create_playlist(payload: PlaylistRequest, request: Request) -> PlaylistResponse:
    provider = request.app.state.provider
    try:
        return await playlist_service.generate_playlist(payload.genre, provider)
    except ProviderUnavailableError:
        raise HTTPException(status_code=502, detail="Could not reach the playlist service.")
