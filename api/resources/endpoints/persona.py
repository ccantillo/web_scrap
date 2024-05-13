from typing import Optional, Annotated

from fastapi import APIRouter, Depends

from resources.modules.auth import user_auth
from resources.modules.utils import gen_response, handle_exception
from resources.modules.persona import PersonasModule

personas_router = APIRouter()


@personas_router.get('/api/personas')
async def get_personas_list(
        token: Annotated[str, Depends(user_auth)],
        identificacion: Optional[str] = None,
        nombre: Optional[str] = None
):
    try:
        filters = {
            "identificacion__icontains": identificacion,
            "nombre__icontains":  nombre,
        }
        filters = {key: value for key, value in filters.items() if value is not None and value != 'null'}

        personas = await PersonasModule.get_personas(**filters)
        return await gen_response(personas, False, "List of Personas")

    except Exception as err:
        return await handle_exception(err)


@personas_router.get('/api/personas/{persona_id}')
async def get_persona_details(
        token: Annotated[str, Depends(user_auth)],
        persona_id: str):
    try:
        persona = await PersonasModule.get(persona_id=persona_id)
        return await gen_response(persona, False, "Persona details")

    except Exception as err:
        return await handle_exception(err)
