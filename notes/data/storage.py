import sqlalchemy as sa
import sqlalchemy.orm as orm
from typing import List
from datetime import datetime
from .basemetadata import SqlAlchemyBase
from .page import Page
from .history import History
from . import __all_models  # noqa: F401

__main_storage = None


def main_storage():
    return __main_storage


def init_main_storage(connection_string):
    global __main_storage
    __main_storage = Storage(connection_string)


def current_time():
    return datetime.now()


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

            page.updated_at = current_time()
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
