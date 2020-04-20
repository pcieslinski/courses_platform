import pytest
from typing import Tuple
from mock import Mock, patch

from tests.factories import UserRecord


@pytest.fixture
def db() -> Mock:
    db = Mock()

    db.query.return_value.filter.return_value.delete.return_value = 1
    db.query.return_value.options.return_value.filter.return_value.first.return_value = UserRecord('1',
                                                                                                   'test@gmail.com',
                                                                                                   [])
    db.query.return_value.options.return_value.all.return_value = [
        UserRecord('1', 'test@gmail.com', []),
        UserRecord('2', 'sample@gmail.com', [])
    ]

    return db


@pytest.fixture(scope='function')
@patch('app.persistence.database.session', autospec=True)
def mock_session_with_db(session: Mock, db: Mock) -> Tuple[Mock, Mock]:
    session.return_value.__enter__.return_value = db
    return session, db
