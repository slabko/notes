import os
import flask
import notes.services.registry_service

app = flask.Flask(__name__)


def main():
    register_blueprints()
    setup_db()
    setup_uploads()
    app.run()


def setup_db():
    current_directory = os.getcwd()
    db_path = os.path.join(current_directory, 'notes.sqlite')
    notes.services.registry_service.init_main_service('sqlite:///' + db_path)


def setup_uploads():
    current_directory = os.getcwd()
    uploads_path = os.path.join(current_directory, 'attachemtns/')
    print(uploads_path)
    notes.data.uploads.init_main_service(uploads_path)


def register_blueprints():
    from notes.views.index import index
    app.register_blueprint(index.blueprint)

    from notes.views.pages import pages
    app.register_blueprint(pages.blueprint)


if __name__ == '__main__':
    main()
