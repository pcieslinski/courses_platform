import json
from uuid import uuid4
from typing import Tuple

from app.domain.course import Course
from app.serializers import json_course_serializer as ser


def create_course() -> Tuple[Course, str]:
    course_id = str(uuid4())

    return Course(id=course_id, name='Test Course'), course_id


def test_serialize_user_entity():
    course, course_id = create_course()
    course_json = json.dumps(course, cls=ser.CourseJsonEncoder)

    expected = f'''
        {{"id": "{course_id}",
        "name": "Test Course"}}
    '''

    assert json.loads(course_json) == json.loads(expected)
