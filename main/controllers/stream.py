from flask import jsonify

from main import Config, app
from main.commons.decorators import validate_data
from main.commons.exceptions import NotFound
from main.engines import stream as stream_engine
from main.schemas.base import PaginationSchema
from main.schemas.stream import StreamPatchSchema, StreamSchema


@app.post("/streams")
@validate_data(StreamSchema)
def create_stream(data):
    stream = stream_engine.create_stream(data)

    return StreamSchema().dump(stream)


@app.get("/streams")
@validate_data(PaginationSchema)
def get_streams(data):
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
def get_stream(id):
    stream = stream_engine.get_stream_by_id(id)

    if not stream:
        raise NotFound(error_message=f"Stream with id = {id} is not found")

    return StreamSchema().dump(stream)


@app.put("/streams/<int:id>")
@validate_data(StreamSchema)
def update_stream(data, id):
    stream = stream_engine.get_stream_by_id(id)

    if not stream:
        raise NotFound(error_message=f"Stream with id={id} is not found")

    stream = stream_engine.update_stream(stream, data)

    return StreamSchema().dump(stream)


@app.patch("/streams/<int:id>")
@validate_data(StreamPatchSchema)
def patch_stream(data, id):
    stream = stream_engine.get_stream_by_id(id)

    if not stream:
        raise NotFound(error_message=f"Stream with id={id} is not found")

    stream = stream_engine.update_stream(stream, data)

    return StreamPatchSchema().dump(stream)


@app.delete("/streams/<int:id>")
def delete_stream(id):
    stream = stream_engine.get_stream_by_id(id)

    if not stream:
        raise NotFound(error_message=f"Stream with id={id} is not found")

    stream_engine.delete_stream(stream)

    return jsonify({"message": f"Stream with id = {id} has been deleted"})
