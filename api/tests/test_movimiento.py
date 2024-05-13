import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from app import app
from resources.models import Movimiento
from resources.modules.auth import validate_user
from resources.modules.movimiento import MovimientosModule

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
async def test_get_movimientos(client: AsyncClient):  # nosec
    response = await client.get("/api/movimientos", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    data = data.get('result')
    assert isinstance(data, list) is True


@pytest.mark.anyio
async def test_get_movimiento(client: AsyncClient):  # nosec
    response = await client.get("/api/movimientos/17", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    data = data.get('result')
    assert "id" in data


@pytest.mark.anyio
async def test_get_movimiento_not_found_id(client: AsyncClient):  # nosec
    response = await client.get("/api/movimientos/051515", headers=headers)
    assert response.status_code == 404, response.text
    data = response.json()
    data = data.get('detail')
    assert data["code"] == "P-02"
    assert "error_message" in data
    assert "error_detailed" in data


@pytest.mark.anyio
async def test_get_movimiento_invalid_id(client: AsyncClient):  # nosec
    response = await client.get("/api/movimientos/vsvdsvsd", headers=headers)
    assert response.status_code == 422, response.text


@pytest.mark.anyio
async def test_create_movimiento(client: AsyncClient):  # nosec
    movimientos_payload = {
        "fecha": "2024-03-19T20:30:00+00:00",
        "causa_id": 17,
        "judicatura": "UNIDAD JUDICIAL PENAL CON SEDE EN EL CANTÓN BABAHOYO TEST",
        "ofendidos": "test",
        "demandados": "test"
    }
    data = await MovimientosModule.create(**movimientos_payload)
    assert data["judicatura"] == "UNIDAD JUDICIAL PENAL CON SEDE EN EL CANTÓN BABAHOYO TEST"
    assert "id" in data
    movimiento_id = data["id"]

    movimiento_obj = await Movimiento.get(id=movimiento_id)
    assert movimiento_obj.id == movimiento_id