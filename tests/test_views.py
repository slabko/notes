import notes.app
import notes.data.storage
import notes.views.index
from unittest import mock
import notes.app
from .samples import page1

get_pages_target = 'notes.data.storage.Storage.get_pages'
get_page_target = 'notes.data.storage.Storage.get_page'
save_page_target = 'notes.data.storage.Storage.save_page'
renderer_target = 'notes.text_processing.markdown.render'

a_string = 'some markdown result'


def test_index_empty_pages(app, request_templates):
    storage_mock = mock.patch(get_pages_target, return_value=[])
    request_context = app.test_request_context(path='/')
    with storage_mock, request_context, request_templates as ts:
        notes.views.index.index.index()
    template, context = ts[0]
    assert template.name == 'index/index.html'
    assert context['notes'] == []


def test_index_one_page(app, request_templates):
    storage_mock = mock.patch(get_pages_target, return_value=[page1])
    request_context = app.test_request_context(path='/')
    with storage_mock, request_context, request_templates as ts:
        notes.views.index.index.index()
    template, context = ts[0]
    assert template.name == 'index/index.html'
    assert context['notes'] == [page1]


def test_read_page(app, request_templates):
    storage_mock = mock.patch(get_page_target, return_value=page1)
    markdown_mock = mock.patch(renderer_target, return_value=a_string)
    request_context = app.test_request_context(path='/pages/1')
    with storage_mock, markdown_mock, request_context, request_templates as ts:
        notes.views.pages.pages.page(1)
    template, context = ts[0]
    assert template.name == 'pages/page.html'
    assert context['content'] == a_string
    assert context['page'] == page1


def test_edit_page(app, request_templates):
    storage_mock = mock.patch(get_page_target, return_value=page1)
    request_context = app.test_request_context(path='/pages/edit/1')
    with storage_mock, request_context, request_templates as ts:
        notes.views.pages.pages.edit(1)
    template, context = ts[0]
    assert template.name == 'pages/edit.html'
    assert context['page'] == page1


def test_submit_edit(app):
    save_page_mock = mock.patch(save_page_target, return_value=1)
    request_context = app.test_request_context(
        path='/pages/edit/1',
        data={'body': a_string}
    )
    with request_context, save_page_mock as save_page:
        res = notes.views.pages.pages.save(1)

    save_page.assert_called_once_with(a_string, 1)

    assert res.status_code == 302
    assert res.location == '/pages/1'
