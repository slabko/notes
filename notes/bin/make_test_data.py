"""

To run the script call

    PYTHONPATH=$(pwd) python ./notes/bin/test_data.py

"""
import os
from notes.data import storage


def main():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    markdown_path = os.path.join(current_directory, 'page.md')
    with open(markdown_path, 'r') as fp:
        markdown_content = fp.read()

    init_db()
    storage.main_service.save_page(markdown_content)


def init_db():
    current_directory = os.getcwd()
    db_path = os.path.join(current_directory, 'notes.sqlite')
    db_path = os.path.abspath(db_path)
    storage.init_main_service('sqlite:///' + db_path)


if __name__ == "__main__":
    main()
