from werkzeug.security import check_password_hash, generate_password_hash

from main import db
from main.models.user import UserModel


def get_user_by_id(id: int) -> UserModel:
    return UserModel.query.get(id)


def get_user_by_email(email: str) -> UserModel:
    return UserModel.query.filter_by(email=email).first()


def create_user(data: dict) -> UserModel:
    password_hash = generate_password_hash(data["password"])

    user = UserModel(
        email=data["email"],
        password_hash=password_hash,
        display_name=data["display_name"],
    )

    db.session.add(user)
    db.session.commit()

    return user


def auth_user_password(user: UserModel, password: str) -> bool:
    return check_password_hash(user.password_hash, password)


def update_user(data: dict, user: UserModel) -> UserModel:
    user.display_name = data["display_name"]

    db.session.commit()

    return user
