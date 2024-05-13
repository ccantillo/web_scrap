import os
from typing import List, Dict

from tortoise.expressions import Q

from resources.exceptions.exceptions import DoesNotExist, DuplicateUser
from resources.models import User
from resources.modules.auth import hash_password
from resources.schemas.users import UserSchema


class UsersModule:
    @staticmethod
    async def create(**kwargs: any) ->Dict:
        existing_user = await User.get_or_none(username=kwargs.get('username'))
        if existing_user:
            raise DuplicateUser

        validated_user_payload = UserSchema().load(kwargs, unknown='exclude')

        new_salt = os.urandom(16)
        password_hash = await hash_password(kwargs.get('password'), new_salt)
        validated_user_payload["password"] = password_hash
        validated_user_payload["password_salt"] = new_salt
        user = await User.create(**validated_user_payload)
        user_dict = UserSchema().dump(user)
        return user_dict

    async def create_initial_user(self):
        try:
            initial_user_payload = {
                "username": os.getenv('initial_username'),
                "password": os.getenv('initial_password')
            }
            await self.create(**initial_user_payload)
            print('created user')
        except Exception as e:
            pass
