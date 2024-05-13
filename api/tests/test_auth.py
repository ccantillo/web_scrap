import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from app import app
from resources.models import Causa
from resources.modules.causa import CausasModule


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def client():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            yield c


@pytest.mark.anyio
async def test_get_causas(client: AsyncClient):  # nosec
    response = await client.post("/api/login", json={"username": "admin", "password": "P@ssW0rd"})
    assert response.status_code == 200, response.text
    data = response.json()
    data = data.get('result')
    assert "access_token" in data