import flask
from notes.services.registry_service import main_service

blueprint = flask.Blueprint('index', __name__, template_folder='templates')


@blueprint.route('/')
def index():
    pages = main_service().get_pages()
    return flask.render_template('index/index.html', notes=pages)
