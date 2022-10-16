from marshmallow import fields

from .base import BaseSchema


class GoogleSchema(BaseSchema):
    google_token = fields.String(required=True)
