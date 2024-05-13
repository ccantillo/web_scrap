from typing import List, Dict
from resources.exceptions.exceptions import DoesNotExist
from resources.models import Movimiento
from resources.schemas.actuaciones import ActuacionesSchema
from resources.schemas.movimiento import MovimientoSchema


class MovimientosModule:
    @staticmethod
    async def get(movimiento_id: int) -> Dict:
        movimiento = await Movimiento.get_or_none(id=movimiento_id).prefetch_related('actuaciones')

        if not movimiento:
            raise DoesNotExist(f"Movimiento with ID {movimiento_id} not found.")

        movimiento_dict = MovimientoSchema().dump(movimiento)
        movimiento_dict['actuaciones'] = ActuacionesSchema().dump(movimiento.actuaciones, many=True)
        return movimiento_dict

    @staticmethod
    async def get_movimientos(offset: int = 0, limit: int = 30, **kwargs: any) -> List[Dict]:
        movimientos = await Movimiento.filter(**kwargs)
        movimientos_dicts = MovimientoSchema().dump(movimientos, many=True)
        return movimientos_dicts

    @staticmethod
    async def create(**kwargs: any) -> Dict:
        validated_json_payload = MovimientoSchema().load(kwargs, unknown='exclude')
        movimiento = await Movimiento.create(**validated_json_payload)
        movimiento_dict = MovimientoSchema().dump(movimiento)
        return movimiento_dict

    @staticmethod
    async def update(movimiento_id=None, **kwargs):

        validated_json_payload = MovimientoSchema().load(kwargs, unknown='exclude')
        movimiento = await Movimiento.get(pk=movimiento_id)
        await movimiento.update_from_dict(validated_json_payload).save()

        return MovimientoSchema(unknown='exclude').dump(movimiento)

    @staticmethod
    async def delete(movimiento_id=None):
        movimiento = await Movimiento.get(pk=movimiento_id)
        await movimiento.delete()