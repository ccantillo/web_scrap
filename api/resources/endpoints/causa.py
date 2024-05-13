from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from resources.modules.auth import user_auth
from resources.modules.utils import gen_response, handle_exception
from resources.modules.causa import CausasModule
from typing import Annotated

causas_router = APIRouter()


@causas_router.get('/api/causas')
async def get_causas_list(
        token: Annotated[str, Depends(user_auth)],
        persona: Optional[int] = None,
        fecha_ingreso: Optional[str] = None,
        fecha_ingreso_despues: Optional[str] = None,
        fecha_ingreso_antes: Optional[str] = None,
        num_proceso: Optional[str] = None,
        accion: Optional[str] = None,
        materia: Optional[str] = None,
        asunto: Optional[str] = None,
        tipo_accion: Optional[str] = None,
        tipo_ingreso: Optional[str] = None,
        no_proceso_vinculado: Optional[str] = None,
        tipo_proceso: Optional[str] = None
):
    try:
        filters = {
            "persona_id": persona,
            "fecha_ingreso": fecha_ingreso,
            "fecha_ingreso__gte": fecha_ingreso_despues,
            "fecha_ingreso__lte": fecha_ingreso_antes,
            "num_proceso__icontains": num_proceso,
            "accion__icontains": accion,
            "materia__icontains": materia,
            "asunto__icontains": asunto,
            "tipo_accion__icontains": tipo_accion,
            "tipo_ingreso__icontains": tipo_ingreso,
            "no_proceso_vinculado__icontains": no_proceso_vinculado,
            "tipo_proceso__icontains": tipo_proceso,
        }
        filters = {key: value for key, value in filters.items() if value is not None and value != 'null'}

        causas = await CausasModule.get_causas(**filters)
        return await gen_response(causas, False, "List of Causas")

    except Exception as err:
        return await handle_exception(err)


@causas_router.get('/api/causas/{causa_id}')
async def get_causa_details(
        token: Annotated[str, Depends(user_auth)],
        causa_id: int):
    try:
        causa = await CausasModule.get(causa_id=causa_id)
        return await gen_response(causa, False, "Causa details")

    except Exception as err:
        return await handle_exception(err)
