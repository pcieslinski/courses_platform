import json
from uuid import uuid4
from typing import Tuple

from app.domain.user import User
from app.serializers import json_user_serializer as ser


def create_user() -> Tuple[User, str]:
    user_id = str(uuid4())

    return User(id=user_id, email='test@gmail.com'), user_id


def test_serialize_user_without_courses():
    user, user_id = create_user()

    user_json = json.dumps(user, cls=ser.UserJsonEncoder)

    expected = f'''
        {{"id": "{user_id}",
        "email": "test@gmail.com"}}
    '''

    assert json.loads(user_json) == json.loads(expected)
