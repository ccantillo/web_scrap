import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from app import app
from resources.models import Causa, Actuaciones
from resources.modules.actuaciones import ActuacionesModule
from resources.modules.auth import validate_user

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
async def test_get_actuaciones(client: AsyncClient):  # nosec
    response = await client.get("/api/actuaciones", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    data = data.get('result')
    assert isinstance(data, list) is True


@pytest.mark.anyio
async def test_get_actuacion(client: AsyncClient):  # nosec
    response = await client.get("/api/actuaciones/1", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    data = data.get('result')
    assert "id" in data


@pytest.mark.anyio
async def test_get_actuacion_not_found_id(client: AsyncClient):  # nosec
    response = await client.get("/api/actuaciones/0515156262", headers=headers)
    assert response.status_code == 404, response.text
    data = response.json()
    data = data.get('detail')
    assert data["code"] == "P-02"
    assert "error_message" in data
    assert "error_detailed" in data


@pytest.mark.anyio
async def test_get_actuacion_invalid_id(client: AsyncClient):  # nosec
    response = await client.get("/api/actuaciones/vsvdsvsd", headers=headers)
    assert response.status_code == 422, response.text


@pytest.mark.anyio
async def test_create_actuacion(client: AsyncClient):  # nosec
    actuaciones_payload = {
        "fecha_ingreso": "2024-04-22 16:08:00+00:00",
        "detalle": "CONVOCATORIA AUDIENCIA DE PROCEDIMIENTO DIRECTO (RAZON DE NOTIFICACION)",
        "descripcion": "test",
        "movimiento_id": 17
    }
    data = await ActuacionesModule.create(**actuaciones_payload)
    assert data["detalle"] == "CONVOCATORIA AUDIENCIA DE PROCEDIMIENTO DIRECTO (RAZON DE NOTIFICACION)"
    assert "id" in data
    actuacion_id = data["id"]

    actuacion_obj = await Actuaciones.get(id=actuacion_id)
    assert actuacion_obj.id == actuacion_id