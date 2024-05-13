from marshmallow import Schema, fields
from marshmallow.fields import Int

from resources.schemas.causa import CausaSchema


class MovimientoSchema(Schema):
    id = fields.Int(dump_only=True)
    fecha = fields.DateTime()
    causa_id = fields.Int()
    judicatura = fields.Str()
    ofendidos = fields.Str()
    demandados = fields.Str()