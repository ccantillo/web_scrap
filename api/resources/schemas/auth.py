from marshmallow import Schema, fields


class LoginSchema(Schema):
    id = fields.Int(dump_only=True)
    user_name = fields.Str()
    password = fields.Str()
    fecha_ingreso = fields.Str()
    detalle = fields.Str()
    descripcion = fields.Str(required=False)
    movimiento_id = fields.Int()