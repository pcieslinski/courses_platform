import json
from uuid import uuid4
from typing import Tuple

from courses_platform.domain.course import Course
from courses_platform.serializers import json_user_serializer as ser


def create_stub_user() -> Tuple[object, str, str]:
    user_id = str(uuid4())
    course_id = str(uuid4())

    class StubUser:
        def __init__(self):
            self.id = user_id
            self.email = 'test@gmail.com'
            self.courses = [Course(id=course_id, name='Test Course')]

    return StubUser(), user_id, course_id


def test_serialize_user_entity():
    user, user_id, course_id = create_stub_user()
    user_json = json.dumps(user, cls=ser.UserJsonEncoder)

    expected = f'''
        {{"id": "{user_id}",
        "email": "test@gmail.com",
        "courses": [{{"id": "{course_id}", "name": "Test Course"}}]}}
    '''

    assert json.loads(user_json) == json.loads(expected)
