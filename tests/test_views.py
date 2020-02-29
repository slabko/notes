import io
import notes.app
import notes.services
import notes.views.index
from unittest import mock
import notes.app
from .samples import page1

get_pages_target = 'notes.services.RegistryService.get_pages'
get_page_target = 'notes.services.RegistryService.get_page'
save_page_target = 'notes.services.RegistryService.save_page'
renderer_target = 'notes.text_processing.markdown.render'
upload_file_target = 'notes.services.AttachmentStorage.upload'
list_uploads_target = 'notes.services.AttachmentStorage.list'
delete_file_target = 'notes.services.AttachmentStorage.delete'

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
    request_context = app.test_request_context(path='/pages/1/')
    with storage_mock, markdown_mock, request_context, request_templates as ts:
        notes.views.pages.pages.page(1)
    template, context = ts[0]
    assert template.name == 'pages/page.html'
    assert context['content'] == a_string
    assert context['page'] == page1


def test_edit_page(app, request_templates):
    storage_mock = mock.patch(get_page_target, return_value=page1)
    request_context = app.test_request_context(path='/pages/edit/1/')
    with storage_mock, request_context, request_templates as ts:
        notes.views.pages.pages.edit(1)
    template, context = ts[0]
    assert template.name == 'pages/edit.html'
    assert context['page'] == page1


def test_submit_edit(app):
    save_page_mock = mock.patch(save_page_target, return_value=1)
    request_context = app.test_request_context(
        path='/pages/edit/1/',
        data={'body': a_string}
    )
    with request_context, save_page_mock as save_page:
        res = notes.views.pages.pages.save(1)

    save_page.assert_called_once_with(a_string, 1)

    assert res.status_code == 302
    assert res.location == '/pages/1/'


def test_upload_file_to_page(app):
    file_content = b'file content'
    page_id = 1
    file_stream = io.BytesIO(file_content)
    file_name = 'foo.txt'
    data = {
        'page': str(page_id),
        'file': (file_stream, file_name)
    }

    request_context = app.test_request_context(
        path='/pages/edit/1/attachements/',
        data=data,
        content_type='multipart/form-data'
    )

    stream_output = None

    def save_stream(page_id, file_name, stream):
        nonlocal stream_output
        stream_output = stream.read()

    upload_mock = mock.patch(upload_file_target, side_effect=save_stream)

    with request_context, upload_mock:
        notes.views.pages.pages.upload(1)

    assert stream_output == file_content


def test_uploads_list(app, request_templates):
    files = ['foo.txt', 'bar.txt']
    storage = mock.patch(get_page_target, return_value=page1)
    uploads = mock.patch(list_uploads_target, return_value=files)
    markdown = mock.patch(renderer_target, return_value=a_string)
    request_context = app.test_request_context(path='/pages/1/')

    with storage, uploads, markdown, request_context, request_templates as ts:
        notes.views.pages.pages.page(1)
    template, context = ts[0]

    assert context['files'] == files


def test_delete_file(app):
    file_name = 'foo.txt'
    delete_file_mock = mock.patch(delete_file_target)
    request_context = app.test_request_context(
        path=f'/pages/edit/1/attachements/{file_name}',
    )
    with request_context, delete_file_mock as delete_file:
        res = notes.views.pages.pages.dalete_file(1, file_name)

    delete_file.assert_called_once_with(1, file_name)

    assert res.status_code == 302
    assert res.location == '/pages/1/'
