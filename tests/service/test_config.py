from flask import Flask

from app.service.config import TestConfig, DevConfig, ProdConfig


def test_app_initialize_correctly_with_test_config(app):
    app.config.from_object(TestConfig)

    assert isinstance(app, Flask)

    assert app.config['ENV'] == 'test'
    assert app.config['DEBUG']
    assert app.config['TESTING']


def test_app_initialize_correctly_with_dev_config(app):
    app.config.from_object(DevConfig)

    assert isinstance(app, Flask)

    assert app.config['ENV'] == 'development'
    assert app.config['DEBUG']


def test_app_initialize_correctly_with_prod_config(app):
    app.config.from_object(ProdConfig)

    assert isinstance(app, Flask)

    assert app.config['ENV'] == 'production'
    assert not app.config['DEBUG']
