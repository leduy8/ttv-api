from main import db

from .base import BaseModel


class StreamModel(BaseModel):
    __tablename__ = "streams"

    creator_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(120), nullable=False)

    def __str__(self) -> str:
        return f"<StreamModel {self.name}>"
