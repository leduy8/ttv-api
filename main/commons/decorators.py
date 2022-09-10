import functools

from flask import request
from marshmallow import ValidationError

from main.commons.exceptions import BadRequest
from main.schemas.base import BaseSchema


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
