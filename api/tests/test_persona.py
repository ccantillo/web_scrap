import uuid
import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from app import app
from resources.models import Persona
from resources.modules.auth import validate_user
from resources.modules.persona import PersonasModule

headers = {}


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def client():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        auth_user = await validate_user(username="admin", password="P@ssW0rd")
        headers["Authorization"] = auth_user.get('access_token')
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            yield c


@pytest.mark.anyio
async def test_get_personas(client: AsyncClient):  # nosec
    response = await client.get("/api/personas", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    data = data.get('result')
    assert isinstance(data, list) is True


@pytest.mark.anyio
async def test_get_persona(client: AsyncClient):  # nosec
    response = await client.get("/api/personas/0968599020001", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    data = data.get('result')
    assert data["identificacion"] == "0968599020001"
    assert "id" in data
    persona_id = data["id"]

    persona_obj = await Persona.get(id=persona_id)
    assert persona_obj.id == persona_id


@pytest.mark.anyio
async def test_get_persona_not_found_id(client: AsyncClient):  # nosec
    response = await client.get("/api/personas/00051515", headers=headers)
    assert response.status_code == 404, response.text
    data = response.json()
    data = data.get('detail')
    assert data["code"] == "P-02"
    assert "error_message" in data
    assert "error_detailed" in data


@pytest.mark.anyio
async def test_create_persona(client: AsyncClient):  # nosec
    random_id = str(uuid.uuid4())
    persona_payload = {
        "identificacion": random_id,
        "nombre": "test_nombre"
    }
    data = await PersonasModule.create(**persona_payload)
    assert data["identificacion"] == random_id
    assert "id" in data
    persona_id = data["id"]
    persona_obj = await Persona.get(id=persona_id)
    assert persona_obj.id == persona_id