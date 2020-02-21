import sqlalchemy as sa
import sqlalchemy.orm as orm
from typing import List
from datetime import datetime
from .basemetadata import SqlAlchemyBase
from .page import Page
from .history import History
from .upload import Upload
from . import __all_models  # noqa: F401

__main_service = None


def main_service():
    return __main_service


def init_main_storage(connection_string):
    global __main_service
    __main_service = Storage(connection_string)


class Storage:

    def __init__(self, connection_string):
        engine = sa.create_engine(connection_string, echo=False)
        self.__factory = orm.sessionmaker(bind=engine)
        SqlAlchemyBase.metadata.create_all(engine)

    def save_page(self, body, page_id=None) -> str:
        session = self.__factory()

        if page_id:
            page = session.query(Page).\
                filter(Page.id == page_id).\
                first()

            history = History()
            history.page_id = page.id
            history.body = page.body
            history.updated_at = page.updated_at
            session.add(history)

            page.updated_at = datetime.now()
        else:
            page = Page()
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

    def get_page(self, page_id) -> Page:
        session = self.__factory()
        page = session.query(Page).\
            filter(Page.id == page_id).\
            one()
        return page

    def get_pages(self):
        session = self.__factory()
        pages = session.query(Page).all()
        return pages

    def get_history_for_page(self, page_id) -> List[History]:
        session = self.__factory()
        page = session.query(Page).\
            filter(Page.id == page_id).\
            one()

        history = session.query(History).\
            filter(History.page_id == page.id).\
            all()

        return history

    def register_attachement(self, page_id, file_name, file_id):
        session = self.__factory()
        upload = Upload(
            id=file_id,
            page_id=page_id,
            file_name=file_name
        )
        session.add(upload)

        existing = session.query(Upload).\
            filter(Upload.id == page_id).\
            filter(Upload.file_name == file_name).\
            one()

        if existing:
            existing.delete()


    def get_attachement_file_id(self, page_id, file_name) -> str:
        session = self.__factory()
        upload = session.query(Upload).\
            filter(Upload.id == page_id).\
            filter(Upload.file_name == file_name).\
            one()

        return upload.id
