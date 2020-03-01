import sqlalchemy as sa
from datetime import datetime
from .basemetadata import SqlAlchemyBase


class Attachment(SqlAlchemyBase):
    __tablename__ = 'attachments'

    id = sa.Column(
        sa.String,
        primary_key=True
    )

    page_id = sa.Column(
        sa.Integer,
        nullable=False,
        index=True
    )

    file_name = sa.Column(
        sa.String,
        nullable=False,
        index=True
    )

    created_at = sa.Column(
        sa.DateTime(),
        index=True,
        nullable=False,
        default=datetime.now
    )

    def __repr__(self):
        return f'Upload({self.id}, {self.page_id}, {self.file_name})'
