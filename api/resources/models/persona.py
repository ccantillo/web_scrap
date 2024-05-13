from tortoise import fields
from tortoise.models import Model


class Persona(Model):
    id = fields.IntField(pk=True)
    identificacion = fields.CharField(max_length=45, unique=True)
    nombre = fields.CharField(max_length=200, null=True)
