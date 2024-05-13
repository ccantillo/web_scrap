from typing import List, Dict
from resources.exceptions.exceptions import DoesNotExist
from resources.models import Actuaciones
from resources.schemas.actuaciones import ActuacionesSchema


class ActuacionesModule:
    @staticmethod
    async def get(actuacion_id: int) -> Dict:
        actuacion = await Actuaciones.get_or_none(id=actuacion_id)

        if not actuacion:
            raise DoesNotExist(f"Actuacion with ID {actuacion_id} not found.")

        actuacion_dict = ActuacionesSchema().dump(actuacion)
        return actuacion_dict

    @staticmethod
    async def get_actuaciones(offset: int = 0, limit: int = 30, **kwargs: any) -> List[Dict]:
        actuaciones = await Actuaciones.filter(**kwargs)
        actuaciones_dicts = ActuacionesSchema().dump(actuaciones, many=True)
        return actuaciones_dicts

    @staticmethod
    async def create(**kwargs: any) -> Dict:
        validated_json_payload = ActuacionesSchema().load(kwargs, unknown='exclude')
        actuacion = await Actuaciones.create(**validated_json_payload)
        actuacion_dict = ActuacionesSchema().dump(actuacion)
        return actuacion_dict

    @staticmethod
    async def update(actuacion_id=None, **kwargs):

        validated_json_payload = ActuacionesSchema().load(kwargs, unknown='exclude')
        actuacion = await Actuaciones.get(pk=actuacion_id)
        await actuacion.update_from_dict(validated_json_payload).save()

        return ActuacionesSchema(unknown='exclude').dump(actuacion)

    @staticmethod
    async def delete(actuacion_id=None):
        actuacion = await Actuaciones.get(pk=actuacion_id)
        await actuacion.delete()