import pytest
from typing import Tuple
from mock import Mock, patch

from tests.factories import CourseRecord


@pytest.fixture
def db() -> Mock:
    db = Mock()

    db.query.return_value.filter.return_value.delete.return_value = 1
    db.query.return_value.filter.return_value.first.return_value = CourseRecord('1', 'Test Course')
    db.query.return_value.all.return_value = [
        CourseRecord('1', 'Test Course'),
        CourseRecord('2', 'Sample Course')
    ]

    return db


@pytest.fixture(scope='function')
@patch('app.persistence.database.session', autospec=True)
def mock_session_with_db(session: Mock, db: Mock) -> Tuple[Mock, Mock]:
    session.return_value.__enter__.return_value = db
    return session, db
