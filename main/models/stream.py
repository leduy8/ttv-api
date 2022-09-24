from main import db

from .base import BaseModel


class StreamModel(BaseModel):
    __tablename__ = "streams"

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean(), default=False)

    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    creator = db.relationship("UserModel", backref="stream", uselist=False)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    creator = db.relationship("CategoryModel")

    def __str__(self) -> str:
        return f"<StreamModel {self.title}>"
