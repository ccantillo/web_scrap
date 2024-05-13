from typing import Annotated

from fastapi import APIRouter, Depends

from resources.modules.auth import user_auth
from resources.modules.utils import gen_response, handle_exception
from resources.modules.web_scrap import execute_test_case, fill_information

web_scrap_router = APIRouter()


@web_scrap_router.get('/api/llenar_informacion')
async def llenar_informacion(token: Annotated[str, Depends(user_auth)],):
    try:
        await fill_information(['0968599020001'])
        return await gen_response(None, False, "processing information")

    except Exception as err:
        return await handle_exception(err)


@web_scrap_router.get('/api/llenar_informacion/{persona_id}')
async def llenar_informacion(token: Annotated[str, Depends(user_auth)], persona_id: str):
    try:
        await fill_information(persona_id)
        return await gen_response(None, False, "processing information")

    except Exception as err:
        return await handle_exception(err)
