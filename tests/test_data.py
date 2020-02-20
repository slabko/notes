import pytest
import datetime
from notes.data.storage import Storage


@pytest.fixture
def storage() -> Storage:
    return Storage('sqlite://')


@pytest.fixture
def set_datetime(monkeypatch):
    def patch_datetime(current_time):
        monkeypatch.setattr(datetime.datetime, 'now', lambda: current_time)

    return patch_datetime


def test_multiline_article(storage: Storage):
    body = 'foo\nbar'
    id = storage.save_page(body)

    page = storage.get_page(id)
    assert page.title == 'foo'
    assert page.body == body
    assert page.preview == 'bar'


def test_one_line_article(storage: Storage):
    body = 'foo'
    id = storage.save_page(body)
    page = storage.get_page(id)
    assert page.title == body
    assert not page.preview
    assert page.body == body


def test_article_with_markdown_header(storage: Storage):
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


def test_update_at(storage, set_datetime):
    body1, body2 = 'foo', 'bar'
    id = storage.save_page(body1)
    page = storage.get_page(id)
    created_at = page.created_at

    current_time = created_at + datetime.timedelta(days=1)
    set_datetime(current_time)

    storage.save_page(body2, page_id=id)
    page = storage.get_page(id)
    assert page.body == body2
    assert page.updated_at == current_time


def test_page_history(storage, set_datetime):
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
