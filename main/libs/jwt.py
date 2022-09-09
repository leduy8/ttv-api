import jwt
from flask import request

from main.config import BaseConfig
from main.commons.exceptions import MissingAuthorzationError, InvalidAuthorizationError


def create_access_token(payload: dict, key=BaseConfig.SECRET_KEY) -> str:
    if type(payload) == dict:
        jwt.encode(payload=payload, key=key, algorithm="HS256")

    raise TypeError("Payload must be a dictionary")


def get_jwt_data() -> str:
    auth_header = request.headers.get("Authorization", None)

    if not auth_header:
        raise MissingAuthorzationError("Authorization header not found")

    auth_header_split = auth_header.split(' ')

    if not auth_header.startswith("Bearer ") or len(auth_header_split) != 2:
        raise InvalidAuthorizationError("Authorization header is invalid")

    return auth_header_split[1]


def get_jwt_payload(token: str):
    try:
        return jwt.decode(jwt=token, key=BaseConfig.SECRET_KEY, algorithms=["HS256"])
    except jwt.DecodeError as e:
        raise e
