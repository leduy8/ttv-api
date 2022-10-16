from main import db

from .base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    email = db.Column(db.String(254), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean(), default=False)
    display_name = db.Column(db.String(64), unique=True)
    profile_img = db.Column(db.Text(), default=None)
    is_google_account = db.Column(db.Boolean(), default=False)
    verified_email = db.Column(db.Boolean(), default=False)

    def __str__(self) -> str:
        return f"<User {self.email}>"
