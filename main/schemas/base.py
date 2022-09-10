from marshmallow import EXCLUDE, Schema, fields


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class PaginationSchema(BaseSchema):
    items_per_page = fields.Integer()
    page = fields.Integer()
    total_items = fields.Integer()
