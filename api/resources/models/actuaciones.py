from tortoise import fields
from tortoise.models import Model


class Actuaciones(Model):
    id = fields.IntField(pk=True)
    fecha_ingreso = fields.DatetimeField(null=True)
    detalle = fields.TextField(null=True)
    descripcion = fields.TextField(null=True)
    movimiento = fields.ForeignKeyField('models.Movimiento', related_name='actuaciones')