import pytest
from fastapi.testclient import TestClient

from core.constants import PLAYLIST_SIZE
from main import app


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_valid_genre_returns_200_with_playlist_size_songs(client):
    response = client.post("/api/playlist", json={"genre": "Rock"})
    assert response.status_code == 200
    body = response.json()
    assert len(body["songs"]) == PLAYLIST_SIZE


def test_invalid_genre_returns_422(client):
    response = client.post("/api/playlist", json={"genre": "Polka"})
    assert response.status_code == 422


def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
