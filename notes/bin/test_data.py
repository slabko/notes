"""

To run the script call

    PYTHONPATH=$(pwd) python ./notes/bin/test_data.py

"""
import os
from notes.data import dbsession
from notes.data.page import Page


def main():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    markdown_path = os.path.join(current_directory, 'page.md')
    with open(markdown_path, 'r') as fp:
        markdown_content = fp.read()

    init_db()
    session = dbsession.create_session()

    page = Page()
    title, text = markdown_content.lstrip().split('\n', 1)
    page.title = title.lstrip('# ')
    page.preview = text[:100]
    page.body = markdown_content

    session.add(page)
    session.commit()


def init_db():
    current_directory = os.getcwd()
    db_path = os.path.join(current_directory, 'notes.sqlite')
    db_path = os.path.abspath(db_path)
    dbsession.global_init(db_path)


if __name__ == "__main__":
    main()
