from typing import Optional, Annotated

from fastapi import APIRouter, Depends

from resources.modules.auth import user_auth
from resources.modules.utils import gen_response, handle_exception
from resources.modules.actuaciones import ActuacionesModule

actuaciones_router = APIRouter()


@actuaciones_router.get('/api/actuaciones')
async def get_actuaciones_list(
        token: Annotated[str, Depends(user_auth)],
        fecha_ingreso: Optional[str] = None,
        fecha_ingreso_despues: Optional[str] = None,
        fecha_ingreso_antes: Optional[str] = None,
        detalle: Optional[str] = None,
        descripcion: Optional[str] = None,
        movimiento: Optional[str] = None,
):
    try:
        filters = {
            "fecha_ingreso": fecha_ingreso,
            "fecha_ingreso__gte": fecha_ingreso_despues,
            "fecha_ingreso__lte": fecha_ingreso_antes,
            "detalle__icontains": detalle,
            "descripcion__icontains": descripcion,
            "movimiento_id": movimiento,
        }
        filters = {key: value for key, value in filters.items() if value is not None and value != 'null'}

        actuaciones = await ActuacionesModule.get_actuaciones(**filters)
        return await gen_response(actuaciones, False, "List of Actuaciones")

    except Exception as err:
        return await handle_exception(err)


@actuaciones_router.get('/api/actuaciones/{actuacion_id}')
async def get_actuacion_details(
        token: Annotated[str, Depends(user_auth)],
        actuacion_id: int):
    try:
        actuacion = await ActuacionesModule.get(actuacion_id=actuacion_id)
        return await gen_response(actuacion, False, "Actuacion details")

    except Exception as err:
        return await handle_exception(err)
