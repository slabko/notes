import sqlalchemy as sa
from datetime import datetime
from .basemetadata import SqlAlchemyBase


def default_created_at_int(content):
    created_at = content.current_parameters['created_at']
    return int(created_at.strftime('%Y%m%d%H%M%S'))


def default_updated_at_int(content):
    return content.current_parameters['created_at']


class Article(SqlAlchemyBase):
    __tablename__ = 'articles'

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
        default=default_updated_at_int
    )

    body = sa.Column(
        sa.String,
        nullable=False
    )

    def __repr__(self):
        return (f'Page(id={self.id}, title={self.title}, '
                f'preview={self.preview}, created_at={self.created_at}, '
                f'updated_at={self.updated_at}, body={self.body})')


class ArticleHistory(SqlAlchemyBase):
    __tablename__ = 'article_history'

    id = sa.Column(sa.Integer,
                   primary_key=True,
                   autoincrement=True)
    page_id = sa.Column(sa.String, index=True, nullable=False)
    updated_at = sa.Column(sa.DateTime(), unique=True, index=True)
    body = sa.Column(sa.String, nullable=False)
