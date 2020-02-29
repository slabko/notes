import sqlalchemy as sa
import sqlalchemy.orm as orm
from typing import List
from datetime import datetime
from notes.data.basemetadata import SqlAlchemyBase
from notes.data.article import Article, ArticleHistory
from notes.data.attachment import Attachment
from notes.data import __all_models  # noqa: F401

__main_service = None


def init_main_service(connection_string):
    global __main_service
    __main_service = RegistryService(connection_string)


class RegistryService:

    def __init__(self, connection_string):
        engine = sa.create_engine(connection_string, echo=False)
        self.__factory = orm.sessionmaker(bind=engine)
        SqlAlchemyBase.metadata.create_all(engine)

    def save_page(self, body, page_id=None) -> str:
        session = self.__factory()

        if page_id:
            page = session.query(Article).\
                filter(Article.id == page_id).\
                first()

            if page.body == body:
                return page_id

            history = ArticleHistory()
            history.page_id = page.id
            history.body = page.body
            history.updated_at = page.updated_at
            session.add(history)

            page.updated_at = datetime.now()
        else:
            page = Article()
            session.add(page)

        try:
            title, text = body.lstrip().split('\n', 1)
        except ValueError:
            title, text = body, ''

        page.title = title.lstrip('# ')
        page.preview = text[:100].lstrip()
        page.body = body

        session.commit()
        return page.id

    def get_page(self, page_id) -> Article:
        session = self.__factory()
        page = session.query(Article).\
            filter(Article.id == page_id).\
            one()
        return page

    def get_pages(self):
        session = self.__factory()
        pages = session.query(Article).all()
        return pages

    def get_history_for_page(self, page_id) -> List[ArticleHistory]:
        session = self.__factory()
        page = session.query(Article).\
            filter(Article.id == page_id).\
            one()

        history = session.query(ArticleHistory).\
            filter(ArticleHistory.page_id == page.id).\
            all()

        return history

    def register_attachment(self, page_id, file_name, file_id):
        session = self.__factory()
        upload = Attachment(
            id=file_id,
            page_id=page_id,
            file_name=file_name
        )
        session.add(upload)

        existing = session.query(Attachment).\
            filter(Attachment.id == page_id).\
            filter(Attachment.file_name == file_name).\
            first()

        if existing:
            existing.delete()

        session.commit()

    def get_attachment_file_id(self, page_id, file_name) -> str:
        session = self.__factory()
        upload = session.query(Attachment).\
            filter(Attachment.page_id == page_id).\
            filter(Attachment.file_name == file_name).\
            one()

        return upload.id

    def get_page_attachments(self, page_id) -> List[Attachment]:
        session = self.__factory()

        uploads = session.query(Attachment).\
            filter(Attachment.page_id == page_id).\
            all()

        return uploads

    def delete_attachment(self, page_id, file_name):
        session = self.__factory()

        session.query(Attachment).\
            filter(Attachment.page_id == page_id).\
            filter(Attachment.file_name == file_name).\
            delete()

        session.commit()


def main_service() -> RegistryService:
    if __main_service:
        return __main_service
    else:
        raise Exception('storage main service is not initialized')
