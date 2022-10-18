from flask import current_app, jsonify, redirect, url_for
from flask_dance.contrib.google import google

from main import app
from main.commons.decorators import validate_data
from main.commons.error_handlers import InternalServerError
from main.engines.user import create_user_google, get_user_by_email
from main.schemas.google import GoogleSchema
from main.services.redis import redis_client
from main.utils.jwt import create_access_token


@app.post("/google/login")
@validate_data(GoogleSchema)
def google_login(data: dict):
    user = redis_client.get(data["google_token"])
    user = get_user_by_email(user["email"])

    if user:
        return jsonify({"access_token": create_access_token({"email": user.email})})

    if not google.authorized:
        return redirect(url_for("google.login"))

    res = google.get("/oauth2/v1/userinfo")

    if not res.ok:
        raise InternalServerError(
            error_message="Something's wrong, please try again later"
        )

    user_info = res.json()
    user = get_user_by_email(user_info["email"])

    if not user:
        user = create_user_google(user_info)

    # ? Save only email to redis to save space, because user's data is saved in DB
    redis_client.set(
        current_app.blueprints["google"].token, user_info["email"], ex=604800
    )  # ? 604800 = 1 week

    return jsonify(
        {
            "access_token": create_access_token({"email": user.email}),
            "google_token": current_app.blueprints["google"].token,
        }
    )


@app.get("/google/logout")
@validate_data(GoogleSchema)
def google_logout(data: dict):
    del current_app.blueprints["google"].token
    redis_client.delete(data["google_token"])
    return jsonify({"message": "Logged out"})
