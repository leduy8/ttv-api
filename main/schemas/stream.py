from marshmallow import fields, validate

from .base import BaseSchema


class StreamSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    creator_id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=50))
    description = fields.String(validate=validate.Length(max=120))
    category_id = fields.Integer(required=True)
    is_active = fields.Boolean(dump_only=True)
