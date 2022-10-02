from flask import jsonify

from main import Config, app
from main.commons.decorators import authenticate_user, validate_data
from main.commons.exceptions import AlreadyExists, Forbidden, NotFound
from main.engines import category as category_engine
from main.engines import stream as stream_engine
from main.schemas.base import PaginationSchema
from main.schemas.stream import StreamSchema


@app.post("/streams")
@authenticate_user()
@validate_data(StreamSchema)
def create_stream(data, auth_data):
    if not category_engine.get_category_by_id(data["category_id"]):
        raise NotFound(
            error_message=f"Category with id = {data['category_id']} is not found"
        )

    if stream_engine.get_stream_by_creator_id(auth_data["user"].id):
        raise AlreadyExists(error_message="User can only create 1 stream")

    stream = stream_engine.create_stream(data, auth_data["user"])

    return StreamSchema().dump(stream)


@app.get("/streams")
@authenticate_user()
@validate_data(PaginationSchema)
def get_streams(data, auth_data):
    params = {
        "page": data["page"] if "page" in data else 1,
        "items_per_page": data["items_per_page"]
        if "items_per_page" in data
        else Config.STREAMS_PER_PAGE,
    }

    streams = stream_engine.get_streams(params)

    return jsonify(
        {
            "streams": StreamSchema().dump(streams.items, many=True),
            "items_per_page": params["items_per_page"],
            "page": params["page"],
            "total_items": streams.total,
        }
    )


@app.get("/streams/<int:id>")
@authenticate_user()
def get_stream(auth_data, id):
    stream = stream_engine.get_stream_by_id(id)

    if not stream:
        raise NotFound(error_message=f"Stream with id = {id} is not found")

    return StreamSchema().dump(stream)


@app.put("/streams/<int:id>")
@authenticate_user(check_admin=True)
@validate_data(StreamSchema)
def update_stream(data, auth_data, id):
    if not category_engine.get_category_by_id(data["category_id"]):
        raise NotFound(
            error_message=f"Category with id = {data['category_id']} is not found"
        )

    stream = stream_engine.get_stream_by_id(id)

    if not stream:
        raise NotFound(error_message=f"Stream with id = {id} is not found")

    if auth_data["is_admin"] is not True and auth_data["user"].id != stream.creator_id:
        raise Forbidden(error_message="User can only edit owned stream")

    stream = stream_engine.update_stream(stream, data)

    return StreamSchema().dump(stream)


@app.put("/streams/<int:id>/active")
@authenticate_user(check_admin=True)
def active_stream(auth_data, id):
    stream = stream_engine.get_stream_by_id(id)

    if not stream:
        raise NotFound(error_message=f"Stream with id = {id} is not found")

    if auth_data["is_admin"] is not True and auth_data["user"].id != stream.creator_id:
        raise Forbidden(error_message="User can only edit owned stream")

    stream = stream_engine.toggle_stream_active_status(stream, True)

    return StreamSchema().dump(stream)


@app.put("/streams/<int:id>/inactive")
@authenticate_user()
def inactive_stream(auth_data, id):
    stream = stream_engine.get_stream_by_id(id)

    if not stream:
        raise NotFound(error_message=f"Stream with id = {id} is not found")

    if auth_data["is_admin"] is not True and auth_data["user"].id != stream.creator_id:
        raise Forbidden(error_message="User can only edit owned stream")

    stream = stream_engine.toggle_stream_active_status(stream, False)

    return StreamSchema().dump(stream)


@app.delete("/streams/<int:id>")
@authenticate_user(check_admin=True)
def delete_stream(auth_data, id):
    stream = stream_engine.get_stream_by_id(id)

    if not stream:
        raise NotFound(error_message=f"Stream with id = {id} is not found")

    if auth_data["is_admin"] is not True and auth_data["user"].id != stream.creator_id:
        raise Forbidden(error_message="User can only delete owned stream")

    stream_engine.delete_stream(stream)

    return jsonify({"message": f"Stream with id = {id} has been deleted"})
