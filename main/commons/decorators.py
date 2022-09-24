import functools

from flask import request
from marshmallow import ValidationError

from main.commons.exceptions import BadRequest, Unauthorized
from main.engines.user import get_user_by_email
from main.schemas.base import BaseSchema
from main.utils.jwt import get_jwt_data, get_jwt_payload


def authenticate_user():
    def decorated(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            token = get_jwt_data()
            if not token:
                raise BadRequest(error_message="Invalid token")

            payload = get_jwt_payload(token)
            user = get_user_by_email(payload["email"])

            if not user:
                raise Unauthorized(error_message="Invalid user")

            return f(user, *args, **kwargs)

        return wrapper

    return decorated


def validate_data(schema: BaseSchema):
    def decorated(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            data = None
            try:
                if request.method in ["GET", "DELETE"]:
                    data = schema().load(request.args.to_dict())
                else:
                    data = schema().load(request.get_json())
            except ValidationError as e:
                raise BadRequest(
                    error_data=e.messages, error_message="Invalid input value(s)"
                )

            return f(data, *args, **kwargs)

        return wrapper

    return decorated
