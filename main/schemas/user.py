from marshmallow import fields, validate

from .base import BaseSchema


class AuthUserSchema(BaseSchema):
    email = fields.Email(required=True, validate=validate.Length(min=6, max=254))
    password = fields.String(
        load_only=True, required=True, validate=validate.Length(min=1, max=64)
    )


class FullUserInfoSchema(AuthUserSchema):
    display_name = fields.String(required=True, validate=validate.Length(min=1, max=64))
    profile_img = fields.String(dump_only=True)
    verified_email = fields.Boolean(dump_only=True)
    is_google_account = fields.Boolean(dump_only=True)


class UpdateUserInfoRequestSchema(BaseSchema):
    display_name = fields.String(required=True, validate=validate.Length(min=1, max=64))
