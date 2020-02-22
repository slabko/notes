import io
import os
import uuid
import notes.data.uploads
from unittest import mock
from notes.data.upload import Upload

register_attachement_target = 'notes.data.storage.Storage.register_attachement'
get_file_id_target = 'notes.data.storage.Storage.get_attachement_file_id'
get_files_target = 'notes.data.storage.Storage.get_page_attachments'
delete_file_target = 'notes.data.storage.Storage.delete_attachment'


def test_upload_file_to_page(app):
    file_content_str = 'file content'
    register_attachement_mock = mock.patch(register_attachement_target)

    with register_attachement_mock as register_attachement:
        uploads = notes.data.uploads.main_service()
        file_content = io.BytesIO(file_content_str.encode('utf-8'))
        uploads.upload(1, 'foo.txt', file_content)

        page_dir = os.path.join(app.uploads_path, '1')
        page_files = os.listdir(page_dir)
        assert len(page_files) == 1

        register_attachement.assert_called_once_with(1, 'foo.txt', mock.ANY)

        file_path = os.path.join(page_dir, page_files[0])
        with open(file_path, 'r') as fp:
            assert fp.read() == file_content_str


def test_read_file(app):
    file_id = '5fcc71ce-f6b8-4237-b340-4bed4c818276'
    get_file_id_mock = mock.patch(get_file_id_target, return_value=file_id)
    with get_file_id_mock:
        uploads = notes.data.uploads.main_service()
        res = uploads.read(1, 'foo.txt')
        assert res == os.path.join(app.uploads_path, '1', file_id)


def test_delete(app):
    file_name = 'foo.txt'
    delete_file_mock = mock.patch(delete_file_target)
    with delete_file_mock as delete_file:
        notes.data.uploads.main_service().delete(1, file_name)
    delete_file.assert_called_once_with(1, file_name)


def test_list(app):
    page_id = 1
    items = [Upload(
        id=str(uuid.uuid4()),
        page_id=page_id,
        file_name=f'foo_{x}'
    ) for x in range(3)]

    get_attachements_mock = mock.patch(
        target=get_files_target,
        return_value=items
    )

    with get_attachements_mock:
        uploads = notes.data.uploads.main_service()
        res = uploads.list(page_id)

    assert res == [u.file_name for u in items]
