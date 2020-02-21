import re
from unittest import mock
from .samples import page1, page2

get_pages_target = 'notes.data.storage.Storage.get_pages'
get_page_target = 'notes.data.storage.Storage.get_page'
save_page_target = 'notes.data.storage.Storage.save_page'
renderer_target = 'notes.text_processing.markdown.render'

a_string = 'some markdown result'


def test_empty_index(app):
    storage_mock = mock.patch(get_pages_target, return_value=[])
    with storage_mock, app.test_client() as client:
        res = client.get('/')
    data = res.data.decode('utf-8')

    assert res.status_code == 200
    assert "<a href='/pages/edit/'>Create New</a>" in data


def test_index_with_pages(app):
    pages = [page1, page2]
    storage_mock = mock.patch(get_pages_target, return_value=pages)
    with storage_mock, app.test_client() as client:
        res = client.get('/')
    data = res.data.decode('utf-8')

    assert(res.status_code == 200)

    assert "<a href='/pages/edit/'>Create New</a>" in data

    for p in pages:
        assert f"<a href='/pages/{p.id}'>{p.title}</a>" in data
        assert f'{p.preview}...' in data


def test_read_page(app):
    storage_mock = mock.patch(get_page_target, return_value=page1)
    markdown_mock = mock.patch(renderer_target, return_value=a_string)
    with storage_mock, markdown_mock, app.test_client() as client:
        res = client.get('/pages/1')
    data = res.data.decode('utf-8')

    assert(res.status_code == 200)
    page_content_re = f"<div class='page-content'>\\s+{a_string}\\s*</div>"
    assert re.findall(page_content_re, data)
    assert "<a href='edit/1'>edit</a>" in data


def test_edit_page(app):
    storage_mock = mock.patch(get_page_target, return_value=page1)
    with storage_mock, app.test_client() as client:
        res = client.get('/pages/edit/1')
    data = res.data.decode('utf-8')

    assert(res.status_code == 200)
    page_content = '<textarea name="body" rows="50" cols="120">' +\
                   page1.body +\
                   '</textarea>'
    assert page_content in data
    assert '<form method="POST">' in data
    assert '<input type="submit">' in data


def test_submit_edit(app):
    save_page_mock = mock.patch(save_page_target, return_value=1)
    with save_page_mock, app.test_client() as client:
        res = client.post('/pages/edit/1', data={'body': a_string})

    assert res.status_code == 302
    assert res.location == 'http://localhost/pages/1'
