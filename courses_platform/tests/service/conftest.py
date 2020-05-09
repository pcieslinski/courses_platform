import pytest
from flask import Flask
from typing import Generator
from sqlalchemy.orm import clear_mappers

from app.service import create_app
from app.service.config import TestConfig


FlaskApp = Generator[Flask, None, None]


@pytest.fixture
def app() -> FlaskApp:
    app = create_app(config_object=TestConfig)

    with app.app_context():
        yield app
        clear_mappers()
