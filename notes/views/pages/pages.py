import flask
from datetime import datetime
from notes.text_processing.markdown import render
from notes.data.dbsession import create_session
from notes.data.page import Page
from notes.data.history import History

blueprint = flask.Blueprint(
    'pages',
    __name__,
    template_folder='templates'
)


@blueprint.route('/pages/<created_at_int>')
def page(created_at_int):
    session = create_session()
    page = session.query(Page).\
        filter(Page.created_at_int == created_at_int).\
        first()

    content = render(page.body)
    return flask.render_template('pages/page.html', content=content, page=page)


@blueprint.route('/pages/edit/<created_at_int>', methods=['GET'])
def edit(created_at_int):
    session = create_session()
    page = session.query(Page).\
        filter(Page.created_at_int == created_at_int).\
        first()

    return flask.render_template('pages/edit.html', page=page)


@blueprint.route('/pages/edit/', methods=['GET'])
def edit_new():
    page = Page()
    page.body = ''

    return flask.render_template('pages/edit.html', page=page)


@blueprint.route('/pages/edit/',
                 defaults={'created_at_int': None},
                 methods=['POST'])
@blueprint.route('/pages/edit/<created_at_int>', methods=['POST'])
def save(created_at_int):
    markdown_content = flask.request.form['body']

    session = create_session()

    if created_at_int:
        page = session.query(Page).\
            filter(Page.created_at_int == created_at_int).\
            first()

        history = History()
        history.page_id = page.id
        history.body = page.body
        history.updated_at = page.updated_at
        session.add(history)

    else:
        page = Page()
        session.add(page)

    try:
        title, text = markdown_content.lstrip().split('\n', 1)
    except ValueError:
        title, text = markdown_content, ''

    page.title = title.lstrip('# ')
    page.preview = text[:100]
    page.body = markdown_content
    page.updated_at = datetime.now()

    session.commit()

    return flask.redirect(f'/pages/{page.created_at_int}')
