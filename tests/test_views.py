import pytest
import notes.app
import notes.data.storage
import notes.views.index
from notes.data.page import Page
from datetime import datetime
from unittest import mock

page1 = Page(
    id=1,
    title='foo',
    preview='bar',
    created_at=datetime.now(),
    updated_at=datetime.now(),
    body='foo\nbar'
)

page2 = Page(
    id=1,
    title='bar',
    preview='foo',
    created_at=datetime.now(),
    updated_at=datetime.now(),
    body='bar\nfoo'
)

get_pages_target = 'notes.data.storage.Storage.get_pages'
get_pages_target = 'notes.data.storage.Storage.get_pages'


@pytest.fixture
def app():
    notes.app.app.config['TESTING'] = True
    notes.app.register_blueprints()
    notes.data.storage.init_main_storage('sqlite://')
    return notes.app.app


def test_empty_index_html(app):
    storage_mock = mock.patch(get_pages_target, return_value=[])
    with storage_mock, app.test_client() as client:
        res = client.get('/')
    assert res.status_code == 200
    assert 'Create New' in res.data.decode('utf-8')


def test_empty_index(app):
    storage_mock = mock.patch(get_pages_target, return_value=[])
    request_context = app.test_request_context(path='/')
    with storage_mock, request_context:
        res = notes.views.index.index.index()
    assert len(res) > 0
    assert 'Create New' in res


def test_index_with_one_element(app):
    storage_mock = mock.patch(get_pages_target, return_value=[page1])
    request_context = app.test_request_context(path='/')
    with storage_mock, request_context:
        res = notes.views.index.index.index()
    assert f"<a href='/pages/{page1.id}'>{page1.title}</a>" in res
    assert 'bar..' in res
