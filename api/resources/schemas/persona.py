from marshmallow import Schema, fields


class PersonaSchema(Schema):
    id = fields.Int(dump_only=True)
    identificacion = fields.Str(required=True)
    nombre = fields.Str(required=False)