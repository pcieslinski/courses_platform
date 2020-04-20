import pytest
from flask import Flask

from app.service import create_app
from app.service.config import TestConfig


@pytest.fixture(scope='function')
def app() -> Flask:
    return create_app(config_object=TestConfig)
