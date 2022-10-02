from typing import List

from main import db
from main.models.stream import StreamModel
from main.models.user import UserModel


def create_stream(data: dict, user: UserModel) -> StreamModel:
    stream = StreamModel(
        creator_id=user.id,
        title=data["title"],
        description=data["description"],
        category_id=data["category_id"],
        is_active=False,
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


def get_stream_by_creator_id(creator_id: int) -> StreamModel:
    return StreamModel.query.filter_by(creator_id=creator_id).first()


def update_stream(stream: StreamModel, data: dict):
    stream.title = data["title"] if "title" in data else stream.title
    stream.description = (
        data["description"] if "description" in data else stream.description
    )
    stream.category_id = (
        data["category_id"] if "category_id" in data else stream.category_id
    )

    db.session.commit()

    return stream


def toggle_stream_active_status(stream: StreamModel, is_active: bool):
    stream.is_active = is_active

    return stream


def delete_stream(stream: StreamModel):
    db.session.delete(stream)
    db.session.commit()
