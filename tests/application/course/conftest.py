import pytest
from typing import Tuple
from mock import Mock, patch
from dataclasses import dataclass


@pytest.fixture
def db(course_record: dataclass) -> Mock:
    db = Mock()

    db.query.return_value.filter.return_value.delete.return_value = 1
    db.query.return_value.filter.return_value.first.return_value = course_record('1', 'Test Course')
    db.query.return_value.all.return_value = [
        course_record('1', 'Test Course'),
        course_record('2', 'Sample Course')
    ]

    return db


@pytest.fixture(scope='function')
@patch('app.persistence.database.session', autospec=True)
def mock_session_with_db(session: Mock, db: Mock) -> Tuple[Mock, Mock]:
    session.return_value.__enter__.return_value = db
    return session, db
