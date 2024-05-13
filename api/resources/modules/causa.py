from typing import List, Dict
from resources.exceptions.exceptions import DoesNotExist
from resources.models import Causa
from resources.schemas.causa import CausaSchema
from resources.schemas.movimiento import MovimientoSchema


class CausasModule:
    @staticmethod
    async def get(causa_id: int) -> Dict:
        causa = await Causa.get_or_none(id=causa_id).prefetch_related('movimientos')

        if not causa:
            raise DoesNotExist(f"Causa with ID {causa_id} not found.")

        causa_dict = CausaSchema().dump(causa)
        causa_dict['movimientos'] = MovimientoSchema().dump(causa.movimientos, many=True)
        return causa_dict

    @staticmethod
    async def get_causas(offset: int = 0, limit: int = 30, **kwargs: any) -> List[Dict]:
        causas = await Causa.filter(**kwargs)
        causas_dicts = CausaSchema().dump(causas, many=True)
        return causas_dicts

    @staticmethod
    async def create(**kwargs: any) -> Dict:
        validated_json_payload = CausaSchema().load(kwargs, unknown='exclude')
        print('hello')
        causa = await Causa.create(**validated_json_payload)
        print('hello 2')
        causa_dict = CausaSchema().dump(causa)
        return causa_dict

    @staticmethod
    async def update(causa_id=None, **kwargs):

        validated_json_payload = CausaSchema().load(kwargs, unknown='exclude')
        causa = await Causa.get(pk=causa_id)
        await causa.update_from_dict(validated_json_payload).save()

        return CausaSchema(unknown='exclude').dump(causa)

    @staticmethod
    async def delete(causa_id=None):
        causa = await Causa.get(pk=causa_id)
        await causa.delete()