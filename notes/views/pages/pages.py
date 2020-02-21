import flask
from notes.text_processing import markdown
from notes.data.storage import main_service
from notes.data.page import Page
from werkzeug.utils import secure_filename

blueprint = flask.Blueprint(
    'pages',
    __name__,
    template_folder='templates'
)


@blueprint.route('/pages/<page_id>')
def page(page_id):
    page = main_service().get_page(page_id)
    content = markdown.render(page.body)
    return flask.render_template('pages/page.html', content=content, page=page)


@blueprint.route('/pages/edit/<page_id>', methods=['GET'])
def edit(page_id):
    page = main_service().get_page(page_id)
    return flask.render_template('pages/edit.html', page=page)


@blueprint.route('/pages/edit/', methods=['GET'])
def edit_new():
    page = Page()
    page.body = ''

    return flask.render_template('pages/edit.html', page=page)


@blueprint.route('/pages/edit/',
                 defaults={'page_id': None},
                 methods=['POST'])
@blueprint.route('/pages/edit/<page_id>', methods=['POST'])
def save(page_id):
    body = flask.request.form['body']
    page_id = main_service().save_page(body, page_id)
    return flask.redirect(f'/pages/{page_id}')


@blueprint.route('/pages/edit/<page_id>/attachements', methods=['POST'])
def upload(page_id):
    if not 'file' in flask.request.files:
        return 'No file part', 400
    file = flask.request.files['file']
    if not file.filename:
        return 'No file name', 400

    filename = secure_filename(file.name)
    # print(filename, file.stream.read())
    return flask.redirect(f'/pages/{page_id}')
