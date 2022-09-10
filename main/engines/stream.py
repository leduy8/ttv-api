from typing import List

from main import db
from main.models.stream import StreamModel


def create_stream(data: dict) -> StreamModel:
    stream = StreamModel(
        creator_id=data["creator_id"],
        name=data["name"],
        description=data["description"],
    )

    db.session.add(stream)
    db.session.commit()

    return stream


def get_streams(params: dict) -> List[StreamModel]:
    streams = StreamModel.query.paginate(
        params["page"], params["items_per_page"], False
    )

    return streams


def get_stream_by_id(id: int) -> StreamModel:
    return StreamModel.query.get(id)


def update_stream(stream: StreamModel, data: dict):
    stream.creator_id = (
        data["creator_id"] if "creator_id" in data else stream.creator_id
    )
    stream.name = data["name"] if "name" in data else stream.name
    stream.description = (
        data["description"] if "description" in data else stream.description
    )

    db.session.commit()

    return stream


def delete_stream(stream: StreamModel):
    db.session.delete(stream)
    db.session.commit()
