from flask import jsonify

from main import Config, app
from main.commons.decorators import authenticate_user, validate_data
from main.commons.exceptions import AlreadyExists, Forbidden, NotFound
from main.engines import category as category_engine
from main.schemas.base import PaginationSchema
from main.schemas.category import CategorySchema


@app.post("/categories")
@authenticate_user(check_admin=True)
@validate_data(CategorySchema)
def create_category(data, auth_data):
    if not auth_data["is_admin"]:
        raise Forbidden()

    if category_engine.get_category_by_name(data["name"]):
        raise AlreadyExists(
            error_message=f"Category with name = {data['name']} is already exists"
        )

    category = category_engine.create_category(data)

    return CategorySchema().dump(category)


@app.get("/categories")
@authenticate_user()
@validate_data(PaginationSchema)
def get_categories(data, auth_data):
    params = {
        "page": data["page"] if "page" in data else 1,
        "items_per_page": data["items_per_page"]
        if "items_per_page" in data
        else Config.BASE_ITEM_PER_PAGE,
    }

    categorys = category_engine.get_categories(params)

    return jsonify(
        {
            "categories": CategorySchema().dump(categorys.items, many=True),
            "items_per_page": params["items_per_page"],
            "page": params["page"],
            "total_items": categorys.total,
        }
    )


@app.get("/categories/<int:id>")
@authenticate_user()
def get_category(auth_data, id):
    category = category_engine.get_category_by_id(id)

    if not category:
        raise NotFound(error_message=f"Category with id = {id} is not found")

    return CategorySchema().dump(category)


@app.put("/categories/<int:id>")
@authenticate_user(check_admin=True)
@validate_data(CategorySchema)
def update_category(data, auth_data, id):
    if not auth_data["is_admin"]:
        raise Forbidden()

    category = category_engine.get_category_by_id(id)

    if not category:
        raise NotFound(error_message=f"Category with id={id} is not found")

    category = category_engine.update_category(category, data)

    return CategorySchema().dump(category)


@app.delete("/categories/<int:id>")
@authenticate_user(check_admin=True)
def delete_category(auth_data, id):
    if not auth_data["is_admin"]:
        raise Forbidden()

    category = category_engine.get_category_by_id(id)

    if not category:
        raise NotFound(error_message=f"Category with id={id} is not found")

    category_engine.delete_category(category)

    return jsonify({"message": f"Category with id = {id} has been deleted"})
