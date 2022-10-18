from main import db

from .base import BaseModel


class ChatModel(BaseModel):
    __tablename__ = "chats"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel", backref="chat")

    stream_id = db.Column(db.Integer, db.ForeignKey("streams.id"))
    stream = db.relationship("StreamModel", backref="chat")

    content = db.Column(db.String(128), nullable=False)

    def __str__(self) -> str:
        return f"<ChatModel {self.id}>"
