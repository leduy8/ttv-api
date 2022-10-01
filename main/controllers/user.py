from flask import jsonify

from main import app
from main.commons.decorators import authenticate_user, validate_data
from main.commons.exceptions import BadRequest
from main.engines import user as user_engine
from main.schemas.user import (
    AuthUserSchema,
    FullUserInfoSchema,
    UpdateUserInfoRequestSchema,
)
from main.utils.jwt import create_access_token


@app.post("/register")
@validate_data(FullUserInfoSchema)
def register_user(data):
    user = user_engine.create_user(data)

    return FullUserInfoSchema().dumps(user)


@app.post("/login")
@validate_data(AuthUserSchema)
def login_user(data):
    user = user_engine.get_user_by_email(data["email"])

    if not user:
        raise BadRequest(error_message="User is already exists")

    if not user_engine.auth_user_password(user, data["password"]):
        raise BadRequest(error_message="Wrong password")

    return jsonify({"access_token": create_access_token({"email": user.email})})


@app.put("/users/update")
@authenticate_user()
@validate_data(UpdateUserInfoRequestSchema)
def update_user(data, user):
    user = user_engine.update_user(data, user)

    return FullUserInfoSchema().dumps(user)
