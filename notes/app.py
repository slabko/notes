import os
import flask
import sqlalchemy
import sqlalchemy.orm
import notes.services.registry_service

app = flask.Flask(__name__)


def main():
    configure()
    app.run()


def configure():
    register_blueprints()
    setup_db()
    setup_uploads()


def setup_db():
    try:
        connection_string = os.environ['NOTES_DB']
    except KeyError:
        current_directory = os.getcwd()
        db_path = os.path.join(current_directory, 'notes.sqlite')
        connection_string = 'sqlite:///' + db_path

    engine = sqlalchemy.create_engine(connection_string, echo=False)
    session_maker = sqlalchemy.orm.sessionmaker(bind=engine)
    notes.services.registry_service.init_main_service(session_maker)


def setup_uploads():
    try:
        attachments_path = os.environ['NOTES_ATTACHMENTS']
    except KeyError:
        current_directory = os.getcwd()
        attachments_path = os.path.join(current_directory, 'attachmetns/')

    notes.services.attachment_service.init_main_service(attachments_path)


def register_blueprints():
    from notes.views.index import index
    app.register_blueprint(index.blueprint)

    from notes.views.pages import pages
    app.register_blueprint(pages.blueprint)


if __name__ == '__main__':
    main()
else:
    configure()
