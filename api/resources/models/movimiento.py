from tortoise import fields
from tortoise.models import Model


class Movimiento(Model):
    id = fields.IntField(pk=True)
    fecha = fields.DatetimeField(null=True)
    causa = fields.ForeignKeyField('models.Causa', related_name='movimientos')
    judicatura = fields.TextField(null=True)
    ofendidos = fields.TextField(null=True)
    demandados = fields.TextField(null=True)