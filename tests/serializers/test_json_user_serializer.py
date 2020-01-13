import json
from uuid import uuid4
from typing import Tuple

from courses_platform.serializers import json_user_serializer as ser


def create_stub_user() -> Tuple[object, str]:
    user_id = str(uuid4())

    class StubUser:
        def __init__(self):
            self.id = user_id
            self.email = 'test@gmail.com'

    return StubUser(), user_id


def test_serialize_user_entity():
    user, user_id = create_stub_user()
    user_json = json.dumps(user, cls=ser.UserJsonEncoder)

    expected = f'''
        {{"id": "{user_id}",
        "email": "test@gmail.com"}}
    '''

    assert json.loads(user_json) == json.loads(expected)
