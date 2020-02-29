import pytest
from contextlib import contextmanager
import notes.app
import notes.services.registry_service
import notes.services.attachment_service
import notes.views.index
from flask import template_rendered
from tempfile import TemporaryDirectory


@pytest.fixture
def app():
    notes.app.app.config['TESTING'] = True
    notes.app.register_blueprints()
    notes.services.registry_service.init_main_service('sqlite://')

    with TemporaryDirectory() as temp_dir:
        notes.services.attachment_service.init_main_service(temp_dir)
        notes.app.app.uploads_path = temp_dir
        yield notes.app.app


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
