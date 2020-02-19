import sqlalchemy as sa
from .basemetadata import SqlAlchemyBase


class History(SqlAlchemyBase):
    __tablename__ = 'history'

    id = sa.Column(sa.Integer,
                   primary_key=True,
                   autoincrement=True)
    page_id = sa.Column(sa.String, index=True, nullable=False)
    updated_at = sa.Column(sa.DateTime(), unique=True, index=True)
    body = sa.Column(sa.String, nullable=False)
