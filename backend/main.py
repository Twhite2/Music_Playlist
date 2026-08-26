from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from core.config import get_settings
from services.providers import build_provider


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.provider = build_provider(get_settings())
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().allowed_origins_list,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}
