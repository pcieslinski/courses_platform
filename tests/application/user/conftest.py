import pytest
from typing import Tuple
from mock import Mock, patch

from app.domain.user import User


@pytest.fixture
def db() -> Mock:
    db = Mock()

    db.query.return_value.filter_by.return_value.first.return_value = User(id='1',
                                                                           email='test@gmail.com')
    db.query.return_value.all.return_value = [
        User(id='1', email='test@gmail.com'),
        User(id='2', email='sample@gmail.com')
    ]

    return db


@pytest.fixture(scope='function')
@patch('app.persistence.session', autospec=True)
def mock_session_with_db(session: Mock, db: Mock) -> Tuple[Mock, Mock]:
    session.return_value.__enter__.return_value = db
    return session, db
