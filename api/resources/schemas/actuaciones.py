from marshmallow import Schema, fields

from resources.schemas.movimiento import MovimientoSchema


class ActuacionesSchema(Schema):
    id = fields.Int(dump_only=True)
    fecha_ingreso = fields.Str()
    detalle = fields.Str()
    descripcion = fields.Str(required=False)
    movimiento_id = fields.Int()