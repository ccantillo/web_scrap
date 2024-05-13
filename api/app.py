import asyncio

from dotenv import load_dotenv
from tortoise.contrib.fastapi import register_tortoise

from resources.endpoints.auth import auth_router
from resources.endpoints.persona import personas_router
from resources.endpoints.actuaciones import actuaciones_router
from resources.endpoints.causa import causas_router
from resources.endpoints.movimiento import movimientos_router
from resources.endpoints.web_scrap import web_scrap_router
import os
import uvicorn

from fastapi import FastAPI

from resources.modules.actuaciones import ActuacionesModule
from resources.modules.causa import CausasModule
from resources.modules.movimiento import MovimientosModule
from resources.modules.persona import PersonasModule
from resources.modules.users import UsersModule
from resources.modules.web_scrap import fill_information

load_dotenv()


app = FastAPI()


# init Database connection

mysql_server_host = os.getenv('db_host')
mysql_server_port = os.getenv('db_port')
mysql_server_password = os.getenv('db_password')
mysql_server_username = os.getenv('db_username')
mysql_db_name = os.getenv('db_name')

db_url = f"mysql://{mysql_server_username}:{mysql_server_password}@{mysql_server_host}:{mysql_server_port}/{mysql_db_name}"

config_db = {
    "connections": {
        "default": db_url
    },
    "apps": {
        "models": {
            "models": ["resources.models"],
            "default_connection": "default"
        }
    }
}

register_tortoise(
    app,
    config=config_db,
    modules={"models": ["resources.models"]},
    generate_schemas=True
)

app.include_router(auth_router)
app.include_router(personas_router)
app.include_router(actuaciones_router)
app.include_router(causas_router)
app.include_router(movimientos_router)
app.include_router(web_scrap_router)


@app.on_event("startup")
async def startup_event():
    await UsersModule().create_initial_user()
    personas = await PersonasModule.get_personas(limit=20)
    causas = await CausasModule.get_causas(limit=20)
    movimientos = await MovimientosModule.get_movimientos(limit=20)
    actuaciones = await ActuacionesModule.get_actuaciones(limit=20)
    if personas and causas and movimientos and actuaciones:
        print("aborting")
        return
    asyncio.create_task(
        fill_information(['0968599020001'])
    )

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="info")