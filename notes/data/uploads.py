import os
import uuid
import shutil
from typing import List
from pathlib import Path
from . import storage

__main_service = None


def main_service():
    return __main_service


class Uploads:

    def __init__(self, path: str):
        self.__path = path

    def list(self, page_id) -> List[str]:
        pass

    def upload(self, page_id, file_name, stream):
        file_id = str(uuid.uuid4())
        page_path = os.path.join(self.__path, str(page_id))
        file_path = os.path.join(page_path, file_id)
        Path(page_path).mkdir(parents=True, exist_ok=True)

        with open(file_path, 'wb') as fp:
            shutil.copyfileobj(stream, fp)

        storage_service = storage.main_service()
        storage_service.register_attachement(page_id, file_name, file_id)

    def read(self, page_id, file_name) -> str:
        storage_service = storage.main_service()
        file_path = storage_service.get_attachement_file_id(page_id, file_name)
        return file_path
