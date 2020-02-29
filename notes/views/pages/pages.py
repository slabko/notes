import flask
import mimetypes
from notes.text_processing import markdown
from notes.services.registry_service import main_service as storage_service
from notes.services.attachment_service import main_service as uploads_service
from notes.data.article import Article
from werkzeug.utils import secure_filename

blueprint = flask.Blueprint(
    'pages',
    __name__,
    template_folder='templates'
)


@blueprint.route('/pages/<int:page_id>/')
def page(page_id):
    page = storage_service().get_page(page_id)
    files = uploads_service().list(page_id)
    content = markdown.render(page.body)
    return flask.render_template(
        'pages/page.html',
        content=content,
        page=page,
        files=files
    )


@blueprint.route('/pages/edit/<int:page_id>/', methods=['GET'])
def edit(page_id):
    page = storage_service().get_page(page_id)
    return flask.render_template('pages/edit.html', page=page)


@blueprint.route('/pages/edit/', methods=['GET'])
def edit_new():
    page = Article()
    page.body = ''

    return flask.render_template('pages/edit.html', page=page)


@blueprint.route('/pages/edit/', defaults={'page_id': None}, methods=['POST'])
@blueprint.route('/pages/edit/<int:page_id>/', methods=['POST'])
def save(page_id):
    body = flask.request.form['body']
    page_id = storage_service().save_page(body, page_id)
    return flask.redirect(f'/pages/{page_id}/')


@blueprint.route('/pages/edit/<int:page_id>/attachements/', methods=['POST'])
def upload(page_id):
    if 'file' not in flask.request.files:
        return 'No file part', 400
    file = flask.request.files['file']
    file_name = file.filename
    if not file_name:
        return 'No file name', 400

    filename = secure_filename(file_name)
    uploads_service().upload(page_id, filename, file.stream)
    return flask.redirect(f'/pages/{page_id}/')


@blueprint.route('/pages/<int:page_id>/<file_name>', methods=['GET'])
@blueprint.route('/pages/edit/<int:page_id>/<file_name>', methods=['GET'])
def read_file(page_id, file_name):
    file_path = uploads_service().read(page_id, file_name)
    mime_type, _ = mimetypes.guess_type(file_name)
    return flask.send_file(file_path, mimetype=mime_type)


@blueprint.route('/pages/edit/<int:page_id>/attachements/<file_name>/delete',
                 methods=['POST'])
def dalete_file(page_id, file_name):
    uploads_service().delete(page_id, file_name)
    return flask.redirect(f'/pages/{page_id}/')
