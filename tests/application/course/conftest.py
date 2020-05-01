import pytest
from typing import Tuple
from mock import Mock, patch

from app.domain.course import Course


@pytest.fixture
def db() -> Mock:
    db = Mock()

    db.query.return_value.filter_by.return_value.first.return_value = Course(id='1', name='Test Course')
    db.query.return_value.all.return_value = [
        Course(id='1', name='Test Course'),
        Course(id='2', name='Sample Course')
    ]

    return db


@pytest.fixture(scope='function')
@patch('app.persistence.session', autospec=True)
def mock_session_with_db(session: Mock, db: Mock) -> Tuple[Mock, Mock]:
    session.return_value.__enter__.return_value = db
    return session, db
