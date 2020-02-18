import flask
from notes.data.page import Page
from notes.data.dbsession import create_session

blueprint = flask.Blueprint('index', __name__, template_folder='templates')


@blueprint.route('/')
def index():
    session = create_session()
    notes = session.query(Page).\
        order_by(Page.created_at.desc())

    return flask.render_template('index/index.html', notes=notes)
