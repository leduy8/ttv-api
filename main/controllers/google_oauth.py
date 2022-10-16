from flask import current_app, jsonify, redirect, url_for
from flask_dance.contrib.google import google

from main import app
from main.commons.decorators import validate_data
from main.commons.error_handlers import InternalServerError
from main.engines.user import create_user_google, get_user_by_email
from main.schemas.google import GoogleSchema
from main.schemas.user import FullUserInfoSchema
from main.services.redis import redis_client


@app.post("/google/login")
@validate_data(GoogleSchema)
def google_login(data: dict):
    user = redis_client.get(data["google_token"])
    user = get_user_by_email(user["email"])

    if user:
        return FullUserInfoSchema.dumps(user)

    if not google.authorized:
        return redirect(url_for("google.login"))

    res = google.get("/oauth2/v1/userinfo")

    if not res.ok:
        raise InternalServerError(
            error_message="Something's wrong, please try again later"
        )

    user_info = res.json()

    if not get_user_by_email(user_info["email"]):
        user = create_user_google(user_info)

    # ? Save only email to redis to save space, because user's data is saved in DB
    redis_client.set(user_info["id"], user_info["email"])

    return FullUserInfoSchema.dumps(user)


@app.get("/google/logout")
@validate_data(GoogleSchema)
def google_logout(data: dict):
    del current_app.blueprints["google"].token
    redis_client.delete(data["google_token"])
    return jsonify("Logged out")
