"""Auth endpoint testlari."""
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch

from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.anyio
async def test_health(client: AsyncClient):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


@pytest.mark.anyio
async def test_register_short_password(client: AsyncClient):
    resp = await client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "short",
    })
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_register_weak_password(client: AsyncClient):
    resp = await client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "alllowercase1234",
    })
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_login_wrong_credentials(client: AsyncClient):
    resp = await client.post("/api/v1/auth/login", json={
        "email": "notexist@example.com",
        "password": "Password123!!",
    })
    assert resp.status_code == 401


@pytest.mark.anyio
async def test_me_without_auth(client: AsyncClient):
    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code == 401


@pytest.mark.anyio
async def test_zones_requires_auth(client: AsyncClient):
    resp = await client.get("/api/v1/zones")
    assert resp.status_code == 401


@pytest.mark.anyio
async def test_signals_requires_auth(client: AsyncClient):
    resp = await client.get("/api/v1/signals")
    assert resp.status_code == 401


@pytest.mark.anyio
async def test_market_symbols(client: AsyncClient):
    resp = await client.get("/api/v1/market/symbols")
    assert resp.status_code == 200
    data = resp.json()
    assert "symbols" in data
    assert "BTCUSDT" in data["symbols"]
