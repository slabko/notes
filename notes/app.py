import os
import flask
import notes.data.storage

app = flask.Flask(__name__)


def main():
    register_blueprints()
    setup_db()
    app.run()


def setup_db():
    current_directory = os.getcwd()
    db_path = os.path.join(current_directory, 'notes.sqlite')
    notes.data.storage.init_main_storage('sqlite:///' + db_path)


def register_blueprints():
    from notes.views.index import index
    app.register_blueprint(index.blueprint)

    from notes.views.pages import pages
    app.register_blueprint(pages.blueprint)


if __name__ == '__main__':
    main()
