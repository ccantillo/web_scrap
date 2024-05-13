from tortoise import fields
from tortoise.models import Model


class Causa(Model):
    id = fields.IntField(pk=True)
    persona = fields.ForeignKeyField('models.Persona', related_name='causas')
    fecha_ingreso = fields.DatetimeField()
    num_proceso = fields.CharField(max_length=45, null=True)
    accion = fields.CharField(max_length=200, null=True)
    materia = fields.CharField(max_length=100, null=True)
    asunto = fields.TextField(null=True)
    tipo_accion = fields.TextField(null=True)
    tipo_ingreso = fields.CharField(max_length=45, null=True)
    no_proceso_vinculado = fields.CharField(max_length=45, null=True)
    tipo_proceso = fields.CharField(max_length=45, null=True)
