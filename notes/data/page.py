import sqlalchemy as sa
from datetime import datetime
from .basemetadata import SqlAlchemyBase


def defulat_created_at_int(content):
    created_at = content.current_parameters['created_at']
    return int(created_at.strftime('%Y%m%d%H%M%S'))


def defulat_updated_at_int(content):
    return content.current_parameters['created_at']


class Page(SqlAlchemyBase):
    __tablename__ = 'pages'

    id = sa.Column(
        sa.Integer,
        primary_key=True,
        autoincrement=True
    )
    title = sa.Column(
        sa.String,
        nullable=False
    )
    preview = sa.Column(
        sa.String,
        nullable=True
    )
    created_at = sa.Column(
        sa.DateTime(),
        index=True,
        nullable=False,
        default=datetime.now
    )
    updated_at = sa.Column(
        sa.DateTime(),
        index=True,
        nullable=False,
        default=defulat_updated_at_int
    )

    body = sa.Column(
        sa.String, 
        nullable=False
    )
