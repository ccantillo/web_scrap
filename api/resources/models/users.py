from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=150, blank=False, null=False, unique=True)
    password = fields.BinaryField(blank=True, null=True)
    password_salt = fields.BinaryField(blank=True, null=True)
