from marshmallow import fields, validate

from .base import BaseSchema


class CategorySchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=128))
    category_img = fields.String()
