import hashlib
from typing import List, Dict, Optional

from fastapi import Header, HTTPException, Request

from resources.exceptions.exceptions import WrongPassword, DoesNotExist, Unauthorized
from resources.models import User
from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv
import os

from resources.schemas.users import UserSchema

load_dotenv()


async def validate_user(username: str, password: str) -> Dict:
    print(f'username was {username}')
    user = await User.get_or_none(username=username)

    if not user:
        raise DoesNotExist(f'Username "{username}" not found')

    if not await compare_password(user, password):
        raise WrongPassword

    user_dict = UserSchema().dump(user)
    user_dict['access_token'] = await generate_jwt_token(user)
    return user_dict


async def hash_password(password, salt):

    password_hash = hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for HMAC
        password.encode('utf-8'),  # Convert the password to bytes
        salt,  # Provide the new salt
        100000,  # It is recommended to use at least 100,000 iterations of SHA-256
        dklen=128  # Get a 128 byte key
    )

    return password_hash


async def compare_password(user: User, password: str) -> bool:
    password_hash = await hash_password(password, user.password_salt)

    return user.password == password_hash


async def generate_jwt_token(User, expsec=None):
    if not expsec:
        expsec = 3600

    exp = datetime.utcnow() + timedelta(seconds=int(expsec))
    payload = {
        'exp': exp,
        'id': str(User.id),
        'iat': datetime.utcnow()
    }
    encoded = jwt.encode(
        payload,
        os.getenv('jwt_secret'),
        algorithm='HS256'
    )
    # decode converts byte string to string, use encode for the reverse:
    return encoded


def jwt_get_payload(token):

    if not token:
        return None

    token = str(token).replace('Bearer ', '').replace('bearer ', '')
    try:
        token_payload = jwt.decode(token, os.getenv('jwt_secret'), algorithms=['HS256'], verify=True)
        return token_payload
    except Exception as e:
        return None


async def user_auth(request: Request, authorization: Optional[str]):
    token = request.headers.get('Authorization') or request.headers.get('authorization') or request.query_params.get('authorization')
    if not token:
        raise HTTPException(status_code=401, detail='Token not found')

    token_payload = jwt_get_payload(token)
    if not token_payload:
        raise HTTPException(status_code=401, detail='Invalid Token')

    user = await User.get_or_none(id=token_payload.get('id'))
    if not user:
        raise HTTPException(status_code=401, detail='User Not Found')

    return UserSchema().dump(user)

