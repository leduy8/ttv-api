from main import db

from .base import BaseModel


class CategoryModel(BaseModel):
    __tablename__ = "categories"

    name = db.Column(db.String(128), unique=True, nullable=False)
    category_img = db.Column(db.Text(), default=None)

    def __str__(self) -> str:
        return f"<CategoryModel {self.name}>"
