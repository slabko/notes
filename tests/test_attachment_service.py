import io
import os
import uuid
import notes.services.attachment_service
from unittest import mock
from notes.data.attachment import Attachment

register_attachment_target = 'notes.services.RegistryService.register_attachment'
get_file_id_target = 'notes.services.RegistryService.get_attachment_file_id'
get_files_target = 'notes.services.RegistryService.get_page_attachments'
delete_file_target = 'notes.services.RegistryService.delete_attachment'


def test_upload_file_to_page(app):
    file_content_str = 'file content'
    register_attachment_mock = mock.patch(register_attachment_target)

    with register_attachment_mock as register_attachment:
        uploads = notes.services.attachment_service.main_service()
        file_content = io.BytesIO(file_content_str.encode('utf-8'))
        uploads.save_attachment(1, 'foo.txt', file_content)

        page_dir = os.path.join(app.uploads_path, '1')
        page_files = os.listdir(page_dir)
        assert len(page_files) == 1

        register_attachment.assert_called_once_with(1, 'foo.txt', mock.ANY)

        file_path = os.path.join(page_dir, page_files[0])
        with open(file_path, 'r') as fp:
            assert fp.read() == file_content_str


def test_read_file(app):
    file_id = '5fcc71ce-f6b8-4237-b340-4bed4c818276'
    get_file_id_mock = mock.patch(get_file_id_target, return_value=file_id)
    with get_file_id_mock:
        uploads = notes.services.attachment_service.main_service()
        res = uploads.get_attachment_path(1, 'foo.txt')
        assert res == os.path.join(app.uploads_path, '1', file_id)


def test_delete(app):
    file_name = 'foo.txt'
    delete_file_mock = mock.patch(delete_file_target)
    with delete_file_mock as delete_file:
        notes.services.attachment_service.main_service().delete_attachment(1, file_name)
    delete_file.assert_called_once_with(1, file_name)


def test_list(app):
    page_id = 1
    items = [Attachment(
        id=str(uuid.uuid4()),
        page_id=page_id,
        file_name=f'foo_{x}'
    ) for x in range(3)]

    get_attachments_mock = mock.patch(
        target=get_files_target,
        return_value=items
    )

    with get_attachments_mock:
        uploads = notes.services.attachment_service.main_service()
        res = uploads.list_attachments(page_id)

    assert res == [u.file_name for u in items]
