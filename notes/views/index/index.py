import flask
from notes.data.storage import main_storage

blueprint = flask.Blueprint('index', __name__, template_folder='templates')


@blueprint.route('/')
def index():
    pages = main_storage().get_pages()

    return flask.render_template('index/index.html', notes=pages)
