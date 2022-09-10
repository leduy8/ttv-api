from marshmallow import fields, validate

from .base import BaseSchema


class BaseStreamSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    creator_id = fields.Integer()
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    description = fields.String(validate=validate.Length(max=120))


class StreamSchema(BaseStreamSchema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))


class StreamPatchSchema(BaseStreamSchema):
    name = fields.String(validate=validate.Length(min=1, max=50))
