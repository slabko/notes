from typing import List
from datetime import datetime
from notes.data.basemetadata import SqlAlchemyBase
from notes.data.article import Article, ArticleHistory
from notes.data.attachment import Attachment
from notes.data import __all_models  # noqa: F401
from contextlib import contextmanager

__main_service = None


def init_main_service(session_maker):
    global __main_service
    __main_service = RegistryService(session_maker)


class RegistryService:

    def __init__(self, session_maker):
        self.__factory = session_maker
        session = self.__factory()
        engine = session.get_bind()
        SqlAlchemyBase.metadata.create_all(engine)

    @contextmanager
    def create_session(self):
        session = self.__factory(expire_on_commit=False)
        try:
            yield session
            session.commit()
        except:  # noqa: E722
            session.rollback()
            raise
        finally:
            session.close()

    def save_page(self, body, page_id=None) -> str:
        with self.create_session() as session:

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
        with self.create_session() as session:
            page = session.query(Article).\
                filter(Article.id == page_id).\
                one()
            return page

    def get_pages(self):
        with self.create_session() as session:
            pages = session.query(Article).all()
            return pages

    def get_history_for_page(self, page_id) -> List[ArticleHistory]:
        with self.create_session() as session:
            page = session.query(Article).\
                filter(Article.id == page_id).\
                one()

            history = session.query(ArticleHistory).\
                filter(ArticleHistory.page_id == page.id).\
                all()

            return history

    def register_attachment(self, page_id, file_name, file_id):
        with self.create_session() as session:

            session.query(Attachment).\
                filter(Attachment.page_id == page_id).\
                filter(Attachment.file_name == file_name).\
                delete()

            upload = Attachment(
                id=file_id,
                page_id=page_id,
                file_name=file_name
            )
            session.add(upload)
            session.commit()

    def get_attachment_file_id(self, page_id, file_name) -> str:
        with self.create_session() as session:
            upload = session.query(Attachment).\
                filter(Attachment.page_id == page_id).\
                filter(Attachment.file_name == file_name).\
                one()

            return upload.id

    def get_page_attachments(self, page_id) -> List[Attachment]:
        with self.create_session() as session:
            uploads = session.query(Attachment).\
                filter(Attachment.page_id == page_id).\
                all()
            return uploads

    def delete_attachment(self, page_id, file_name):
        with self.create_session() as session:
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
