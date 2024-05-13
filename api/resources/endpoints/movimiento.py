from typing import Optional, Annotated

from fastapi import APIRouter, Depends

from resources.modules.auth import user_auth
from resources.modules.utils import gen_response, handle_exception
from resources.modules.movimiento import MovimientosModule

movimientos_router = APIRouter()


@movimientos_router.get('/api/movimientos')
async def get_movimientos_list(
        token: Annotated[str, Depends(user_auth)],
        fecha: Optional[str] = None,
        fecha_despues: Optional[str] = None,
        fecha_antes: Optional[str] = None,
        causa_id: Optional[int] = None,
        judicatura: Optional[str] = None,
        ofendidos: Optional[str] = None,
        demandados: Optional[str] = None,
):
    try:
        filters = {
            "fecha": fecha,
            "fecha__gte": fecha_despues,
            "fecha__lte": fecha_antes,
            "causa_id": causa_id,
            "judicatura__icontains": judicatura,
            "ofendidos__icontains": ofendidos,
            "demandados__icontains": demandados,
        }
        filters = {key: value for key, value in filters.items() if value is not None and value != 'null'}

        movimientos = await MovimientosModule.get_movimientos(**filters)
        return await gen_response(movimientos, False, "List of Movimientos")

    except Exception as err:
        return await handle_exception(err)


@movimientos_router.get('/api/movimientos/{movimiento_id}')
async def get_movimiento_details(movimiento_id: int):
    try:
        movimiento = await MovimientosModule.get(movimiento_id=movimiento_id)
        return await gen_response(movimiento, False, "Movimiento details")

    except Exception as err:
        return await handle_exception(err)
