import pytest
import datetime
from notes.data.storage import Storage
import notes.data.storage


@pytest.fixture
def storage():
    return Storage('sqlite://')


def test_multiline_article(storage: Storage):
    body = '# Test page\n\nhello'
    id = storage.save_page(body)

    page = storage.get_page(id)
    assert page.title == 'Test page'
    assert page.body == body
    assert page.preview == 'hello'


def test_one_line_article(storage: Storage):
    body = 'test'
    id = storage.save_page(body)
    page = storage.get_page(id)
    assert page.title == 'test'
    assert page.body == body


def test_get_all_pages(storage: Storage, monkeypatch):
    body1, body2 = 'foo', 'bar'
    storage.save_page(body1)
    storage.save_page(body2)
    pages = storage.get_pages()

    assert len(pages) == 2
    assert pages[0].body == body1
    assert pages[1].body == body2


def test_page_update(storage: Storage):
    body1, body2 = 'foo\nbar', 'bar\nfoo'
    id = storage.save_page(body1)
    storage.save_page(body2, page_id=id)
    page = storage.get_page(id)
    assert page.body == body2
    assert page.title == 'bar'
    assert page.preview == 'foo'


def test_update_at(storage: Storage, monkeypatch):
    body1, body2 = 'foo', 'bar'
    id = storage.save_page(body1)
    page = storage.get_page(id)
    created_at = page.created_at

    current_time = created_at + datetime.timedelta(days=1)
    monkeypatch.setattr(notes.data.storage,
                        'current_time',
                        lambda: current_time)

    storage.save_page(body2, page_id=id)
    page = storage.get_page(id)
    assert page.body == body2
    assert page.updated_at == current_time


def test_page_history(storage: Storage, monkeypatch):
    body1, body2 = 'foo\nbar', 'bar\nfoo'
    id = storage.save_page(body1)
    page = storage.get_page(id)
    created_at = page.created_at

    current_time = created_at + datetime.timedelta(days=1)
    monkeypatch.setattr(notes.data.storage,
                        'current_time',
                        lambda: current_time)

    storage.save_page(body2, page_id=id)

    history = storage.get_history_for_page(id)

    assert len(history) == 1

    item = history[0]
    assert item.updated_at == created_at
    assert item.body == body1
