import hashlib
from typing import Optional

from fastapi import APIRouter

from resources.modules.auth import validate_user
from resources.modules.utils import gen_response, handle_exception
from resources.modules.persona import PersonasModule
from pydantic import BaseModel


class PayloadModel(BaseModel):
    username: str
    password: str | None = None


auth_router = APIRouter()


@auth_router.post('/api/login')
async def login(payload: PayloadModel):
    try:

        valid_user = await validate_user(username=payload.username, password=payload.password)
        return await gen_response(valid_user, False, "Authorized")
    except Exception as err:
        return await handle_exception(err)


@auth_router.get('/api/personas/{persona_id}')
async def get_persona_details(persona_id: str):
    try:
        persona = await PersonasModule.get(persona_id=persona_id)
        return await gen_response(persona, False, "Persona details")

    except Exception as err:
        return await handle_exception(err)
