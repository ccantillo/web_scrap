import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from app import app
from resources.models import Causa
from resources.modules.auth import validate_user
from resources.modules.causa import CausasModule
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
async def test_get_causas(client: AsyncClient):  # nosec
    response = await client.get("/api/causas", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    data = data.get('result')
    assert isinstance(data, list) is True


@pytest.mark.anyio
async def test_get_causa(client: AsyncClient):  # nosec
    response = await client.get("/api/causas/22", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    data = data.get('result')
    assert "id" in data


@pytest.mark.anyio
async def test_get_causa_not_found_id(client: AsyncClient):  # nosec
    response = await client.get("/api/causas/051515", headers=headers)
    assert response.status_code == 404, response.text
    data = response.json()
    data = data.get('detail')
    assert data["code"] == "P-02"
    assert "error_message" in data
    assert "error_detailed" in data


@pytest.mark.anyio
async def test_get_causa_invalid_id(client: AsyncClient):  # nosec
    response = await client.get("/api/causas/vsvdsvsd", headers=headers)
    assert response.status_code == 422, response.text


@pytest.mark.anyio
async def test_create_causa(client: AsyncClient):  # nosec
    causa_payload = {
        "persona_id": 1,
        "fecha_ingreso": "2023-12-21 13:33:00+00:00",
        "num_proceso": "1781120230264469",
        "accion": "PAGO POR CONSIGNACIÓN",
        "materia": "TRÁNSITO COIP",
        "asunto": "389 CONTRAVENCIONES DE TRÁNSITO DE CUARTA CLASE, INC.1, NUM. 6",
        "tipo_accion": "CONTRAVENCIONES DE TRÁNSITO",
        "tipo_ingreso": "test",
        "no_proceso_vinculado": "test",
        "tipo_proceso": "demandante",
    }
    data = await CausasModule.create(**causa_payload)
    assert data["num_proceso"] == "1781120230264469"
    assert "id" in data
    causa_id = data["id"]

    causa_obj = await Causa.get(id=causa_id)
    assert causa_obj.id == causa_id