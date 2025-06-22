import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from noteapp.main import app

@pytest.mark.asyncio
async def test_create_note():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/notes/", json={
            "title": "Test Note",
            "description": "This is a test note.",
            "tags": ["test", "fastapi"]
        })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Note"
    assert isinstance(data["tags"], list)

@pytest.mark.asyncio
async def test_get_notes():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/notes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
