from main import db

from .base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    email = db.Column(db.String(254), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    display_name = db.Column(db.String(64), unique=True)
    profile_img = db.Column(db.Text(), default=None)

    def __str__(self) -> str:
        return f"<User {self.email}>"
