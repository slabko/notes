import datetime
import pytest
import uuid
from freezegun import freeze_time
from notes.services.registry_service import RegistryService
import sqlalchemy
import sqlalchemy.orm

connection_string = 'sqlite://'
# connection_string = 'postgresql://notes:jb9RBP8k@localhost/notes'


@pytest.fixture
def storage():
    engine = sqlalchemy.create_engine(connection_string)
    session_maker = sqlalchemy.orm.sessionmaker(bind=engine)

    from notes.data.basemetadata import SqlAlchemyBase
    print('\n------> drop all  |\n')
    SqlAlchemyBase.metadata.drop_all(engine)

    print('\n------> ...done |\n')
    return RegistryService(session_maker)


def test_multiline_article(storage: RegistryService):
    body = 'foo\nbar'
    id = storage.save_page(body)

    page = storage.get_page(id)
    assert page.title == 'foo'
    assert page.body == body
    assert page.preview == 'bar'


def test_one_line_article(storage: RegistryService):
    body = 'foo'
    id = storage.save_page(body)
    page = storage.get_page(id)
    assert page.title == body
    assert not page.preview
    assert page.body == body


def test_article_with_markdown_header(storage: RegistryService):
    body = '# foo'
    id = storage.save_page(body)
    page = storage.get_page(id)
    assert page.title == 'foo'


def test_get_all_pages(storage):
    body1, body2 = 'foo', 'bar'
    storage.save_page(body1)
    storage.save_page(body2)
    pages = storage.get_pages()

    assert len(pages) == 2
    assert pages[0].body == body1
    assert pages[1].body == body2


def test_page_update(storage):
    body1, body2 = 'foo\nbar', 'bar\nfoo'
    id = storage.save_page(body1)
    storage.save_page(body2, page_id=id)
    page = storage.get_page(id)
    assert page.body == body2
    assert page.title == 'bar'
    assert page.preview == 'foo'


def test_update_at(storage):
    body1, body2 = 'foo', 'bar'
    id = storage.save_page(body1)
    page = storage.get_page(id)
    created_at = page.created_at

    current_time = created_at + datetime.timedelta(days=1)
    with freeze_time(current_time):
        storage.save_page(body2, page_id=id)

    page = storage.get_page(id)
    assert page.body == body2
    assert page.updated_at == current_time


def test_page_history(storage):
    body1, body2 = 'foo\nbar', 'bar\nfoo'
    id = storage.save_page(body1)
    page = storage.get_page(id)
    created_at = page.created_at

    storage.save_page(body2, page_id=id)

    history = storage.get_history_for_page(id)

    assert len(history) == 1

    item = history[0]
    assert item.updated_at == created_at
    assert item.body == body1


def test_save_without_update_does_not_make_an_update(storage):
    body = 'foo\nbar'
    id = storage.save_page(body)
    page = storage.get_page(id)
    created_at = page.created_at

    current_time = created_at + datetime.timedelta(days=1)
    with freeze_time(current_time):
        storage.save_page(body, page_id=id)

    another = storage.get_page(id)
    assert another.updated_at == page.updated_at
    assert len(storage.get_history_for_page(id)) == 0


def test_attachment(storage: RegistryService):
    file_id = str(uuid.uuid4())
    id = storage.save_page('foobar')
    storage.register_attachment(id, 'foo.txt', file_id)

    res = storage.get_attachment_file_id(id, 'foo.txt')

    assert res == file_id


def test_get_page_attachments(storage: RegistryService):
    print('test_get_page_attachments')
    file_ids = [str(uuid.uuid4()) for x in range(4)]
    file_names = [f'foo_{x}.txt' for x in range(4)]
    page_id = storage.save_page('foobar')
    for file_id, file_name in zip(file_ids, file_names):
        storage.register_attachment(page_id, file_name, file_id)

    # Fake record
    storage.register_attachment(2, 'foo.txt', str(uuid.uuid4()))

    res = storage.get_page_attachments(page_id)

    assert file_ids == [a.id for a in res]
    assert file_names == [a.file_name for a in res]


def test_delete_attachment(storage: RegistryService):
    file_ids = [str(uuid.uuid4()) for x in range(3)]
    file_names = [f'foo_{x}.txt' for x in range(3)]
    id = storage.save_page('foobar')
    for file_id, file_name in zip(file_ids, file_names):
        storage.register_attachment(id, file_name, file_id)

    storage.delete_attachment(id, file_names[1])

    res = storage.get_page_attachments(id)

    file_names = file_names[:1] + file_names[2:]
    stored_file_names = [u.file_name for u in res]
    assert file_names == stored_file_names


def test_attachment_with_the_same_name_is_deleted(storage: RegistryService):
    file_id_1, file_id_2 = str(uuid.uuid4()), str(uuid.uuid4())
    page_id = storage.save_page('foobar')

    storage.register_attachment(page_id, 'foo.txt', file_id_1)
    storage.register_attachment(page_id, 'foo.txt', file_id_2)

    res = storage.get_page_attachments(page_id)
    assert len(res) == 1
    attachment = res[0]
    assert attachment.id == file_id_2
    assert attachment.file_name == 'foo.txt'
