import pytest
from typing import Tuple
from mock import Mock, patch
from dataclasses import dataclass


@pytest.fixture
def db(user_record: dataclass) -> Mock:
    db = Mock()

    db.query.return_value.filter.return_value.delete.return_value = 1
    db.query.return_value.filter.return_value.first.return_value = user_record('1', 'test@gmail.com', [])
    db.query.return_value.all.return_value = [
        user_record('1', 'test@gmail.com', []),
        user_record('2', 'sample@gmail.com', [])
    ]

    return db


@pytest.fixture(scope='function')
@patch('courses_platform.persistence.database.session', autospec=True)
def mock_session_with_db(session: Mock, db: Mock) -> Tuple[Mock, Mock]:
    session.return_value.__enter__.return_value = db
    return session, db
