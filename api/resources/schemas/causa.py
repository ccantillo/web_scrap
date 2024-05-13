from marshmallow import Schema, fields


class CausaSchema(Schema):
    id = fields.Int(dump_only=True)
    persona_id = fields.Int()
    id_info = fields.Int()
    fecha_ingreso = fields.Str(required=True)
    num_proceso = fields.Str()
    accion = fields.Str()
    materia = fields.Str()
    asunto = fields.Str()
    tipo_accion = fields.Str()
    tipo_ingreso = fields.Str()
    no_proceso_vinculado = fields.Str()
    tipo_proceso = fields.Str()