import pytest
from contextlib import contextmanager
import notes.app
import notes.data.storage
import notes.views.index
from notes.data.storage import Storage

from flask import template_rendered
import notes.app


@pytest.fixture
def storage():
    return Storage('sqlite://')


@pytest.fixture
def app():
    notes.app.app.config['TESTING'] = True
    notes.app.register_blueprints()
    notes.data.storage.init_main_storage('sqlite://')
    return notes.app.app


@contextmanager
def __captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)

    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


@pytest.fixture
def request_templates(app):
    return __captured_templates(app)
