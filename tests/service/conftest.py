import pytest
from flask import Flask

from courses_platform.service import create_app
from courses_platform.service.config import TestConfig


@pytest.fixture(scope='function')
def app() -> Flask:
    return create_app(config_object=TestConfig)
