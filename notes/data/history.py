import uuid
import sqlalchemy as sa
from .basemetadata import SqlAlchemyBase


def default_id():
    return str(uuid.uuid4())


class History(SqlAlchemyBase):
    __tablename__ = 'history'

    id = sa.Column(sa.String,
                   primary_key=True,
                   default=default_id)
    page_id = sa.Column(sa.String, index=True, nullable=False)
    updated_at = sa.Column(sa.String, unique=True, index=True)
    body = sa.Column(sa.String, nullable=False)
