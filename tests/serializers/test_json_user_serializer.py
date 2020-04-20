import json
from uuid import uuid4
from typing import Tuple

from tests.factories import StubUser
from app.serializers import json_user_serializer as ser


def create_stub_user() -> Tuple[StubUser, str, str]:
    user_id = str(uuid4())
    course_id = str(uuid4())

    return StubUser(user_id, course_id), user_id, course_id


def test_serialize_user_without_courses():
    user, user_id, course_id = create_stub_user()
    del user.courses

    user_json = json.dumps(user, cls=ser.UserJsonEncoder)

    expected = f'''
        {{"id": "{user_id}",
        "email": "test@gmail.com"}}
    '''

    assert json.loads(user_json) == json.loads(expected)


def test_serialize_user_with_courses():
    user, user_id, course_id = create_stub_user()
    user_json = json.dumps(user, cls=ser.UserJsonEncoder)

    expected = f'''
        {{"id": "{user_id}",
        "email": "test@gmail.com",
        "courses": [{{"id": "{course_id}", "name": "Test Course"}}]}}
    '''

    assert json.loads(user_json) == json.loads(expected)
