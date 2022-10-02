from typing import List

from main import db
from main.models.category import CategoryModel


def create_category(data: dict) -> CategoryModel:
    category = CategoryModel(
        name=data["name"],
    )

    db.session.add(category)
    db.session.commit()

    return category


def get_categories(params: dict) -> List[CategoryModel]:
    categories = CategoryModel.query.paginate(
        params["page"], params["items_per_page"], False
    )

    return categories


def get_category_by_id(id: int) -> CategoryModel:
    return CategoryModel.query.get(id)


def get_category_by_name(name: str) -> CategoryModel:
    return CategoryModel.query.filter_by(name=name).first()


def update_category(category: CategoryModel, data: dict):
    category.name = data["name"] if "name" in data else category.name

    db.session.commit()

    return category


def delete_category(category: CategoryModel):
    db.session.delete(category)
    db.session.commit()
