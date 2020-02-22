import re
import io
from unittest import mock
from .samples import page1, page2

get_pages_target = 'notes.data.storage.Storage.get_pages'
get_page_target = 'notes.data.storage.Storage.get_page'
save_page_target = 'notes.data.storage.Storage.save_page'
renderer_target = 'notes.text_processing.markdown.render'
list_uploads_target = 'notes.data.uploads.Uploads.list'

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
        assert f"<a href='/pages/{p.id}/'>{p.title}</a>" in data
        assert f'{p.preview}...' in data


def test_read_page(app):
    storage_mock = mock.patch(get_page_target, return_value=page1)
    markdown_mock = mock.patch(renderer_target, return_value=a_string)
    with storage_mock, markdown_mock, app.test_client() as client:
        res = client.get('/pages/1/')
    data = res.data.decode('utf-8')

    assert(res.status_code == 200)
    page_content_re = f"<div class='page-content'>\\s+{a_string}\\s*</div>"
    assert re.findall(page_content_re, data)
    assert "<a href='/pages/edit/1/'>edit</a>" in data


def test_upload_controls(app):
    storage_mock = mock.patch(get_page_target, return_value=page1)
    markdown_mock = mock.patch(renderer_target, return_value=a_string)
    with storage_mock, markdown_mock, app.test_client() as client:
        res = client.get('/pages/1/')
    data = res.data.decode('utf-8')

    form_data = (r'<form action="/pages/edit/1/attachements/" '
                 r'method="POST" enctype="multipart/form-data">')
    assert form_data in data
    assert f'<input type="hidden" value="1">' in data
    assert f'<input type="file" name="file" id="file">' in data


def test_edit_page(app):
    storage_mock = mock.patch(get_page_target, return_value=page1)
    with storage_mock, app.test_client() as client:
        res = client.get('/pages/edit/1/')
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
        res = client.post('/pages/edit/1/', data={'body': a_string})

    assert res.status_code == 302
    assert res.location == 'http://localhost/pages/1/'


uploads_path = '/pages/edit/1/attachements/'
form_data = 'multipart/form-data'


def test_upload_file(app):
    data = {
        'page': '1',
        'file': (io.BytesIO(b'file content'), 'file.txt')
    }
    with app.test_client() as client:
        path = uploads_path
        res = client.post(path, data=data, content_type=form_data)

    assert res.status_code == 302
    assert res.location == 'http://localhost/pages/1/'


def test_upload_without_file_part(app):
    data = {'page': '1'}
    with app.test_client() as client:
        res = client.post(uploads_path, data=data, content_type=form_data)

    assert res.status_code == 400


def test_upload_without_file_name(app):
    data = {
        'page': '1',
        'file': (io.BytesIO(b'file content'), '')
    }
    with app.test_client() as client:
        res = client.post(uploads_path, data=data, content_type=form_data)

    assert res.status_code == 400


def test_uploads_list(app):
    files = ['foo.txt', 'bar.txt']
    storage = mock.patch(get_page_target, return_value=page1)
    uploads = mock.patch(list_uploads_target, return_value=files)
    markdown = mock.patch(renderer_target, return_value=a_string)

    with storage, uploads, markdown, app.test_client() as client:
        res = client.get('/pages/1/')
    data = res.data.decode('utf-8')

    for f in files:
        assert f'<a href="/pages/1/{f}">{f}</a>' in data
