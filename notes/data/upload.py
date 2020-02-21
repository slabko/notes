import sqlalchemy as sa
from datetime import datetime
from .basemetadata import SqlAlchemyBase


class Upload(SqlAlchemyBase):
    __tablename__ = 'uploads'

    id = sa.Column(
        sa.String,
        primary_key=True
    )

    file_name = sa.Column(
        sa.String,
        nullable=False
    )

    created_at = sa.Column(
        sa.DateTime(),
        index=True,
        nullable=False,
        default=datetime.now
    )
