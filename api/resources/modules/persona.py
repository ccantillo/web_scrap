from typing import List, Dict

from tortoise.expressions import Q

from resources.exceptions.exceptions import DoesNotExist
from resources.models import Persona
from resources.schemas.persona import PersonaSchema


class PersonasModule:
    @staticmethod
    async def get(persona_id: str) -> Dict:
        persona = await Persona.get_or_none(Q(id=persona_id) | Q(identificacion=persona_id))

        if not persona:
            raise DoesNotExist(f"Persona with ID {persona_id} not found.")

        persona_dict = PersonaSchema().dump(persona)
        return persona_dict

    @staticmethod
    async def get_personas(offset: int = 0, limit: int = 30, **kwargs: any) -> List[Dict]:
        personas = await Persona.filter(**kwargs)
        personas_dicts = PersonaSchema().dump(personas, many=True)
        return personas_dicts

    @staticmethod
    async def create(**kwargs: any) ->Dict:
        validated_json_payload = PersonaSchema().load(kwargs, unknown='exclude')
        persona = await Persona.create(**validated_json_payload)
        persona_dict = PersonaSchema().dump(persona)
        return persona_dict

    @staticmethod
    async def update(persona_id=None, **kwargs):

        validated_json_payload = PersonaSchema().load(kwargs, unknown='exclude')
        persona = await Persona().get(pk=persona_id)
        await persona.update_from_dict(validated_json_payload).save()

        return PersonaSchema(unknown='exclude').dump(persona)

    @staticmethod
    async def delete(persona_id=None):
        persona = await Persona.get(pk=persona_id)
        await persona.delete()
