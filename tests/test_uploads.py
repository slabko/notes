import io
from notes.data.uploads import Uploads
from tempfile import TemporaryDirectory
from unittest import mock

register_attachement_target = 'notes.data.storage.Storage.register_attachement'
get_file_id_target = 'notes.data.storage.Storage.get_attachement_file_id_target'


def test_upload_file_to_page(app):
    register_attachement_mock = mock.patch(register_attachement_target)
    with register_attachement_mock as register_attachement,\
            TemporaryDirectory() as temp_dir:
        uploads = Uploads(temp_dir)
        file_content = io.BytesIO(b'file content')
        uploads.upload(1, 'foo.txt', file_content)
        register_attachement.assert_called_once_with(1, 'foo.txt', mock.ANY)


def test_read_file(app):
    file_id = '5fcc71ce-f6b8-4237-b340-4bed4c818276'
    get_file_id_mock = mock.patch(get_file_id_target, return_value=file_id)
    with register_attachement_mock as register_attachement,
            TemporaryDirectory() as temp_dir:
        uploads = uploads(temp_dir)


# def test_update_file_to_article()
# def test_update_history()
