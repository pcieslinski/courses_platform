import json

import pytest
import requests

from app.adapters.unit_of_work import SqlAlchemyUnitOfWork


def post(api_base_url: str, path: str, data: str) -> requests.Response:
    mimetype = "application/json"
    headers = {
        "Content-Type": mimetype,
        "Accept": mimetype
    }
    return requests.post(f'{api_base_url}{path}', data=data, headers=headers)


@pytest.mark.usefixtures('postgres_db')
def test_withdraw_user_enrollment(postgres_session_factory, api_base_url):
    user_data = json.dumps(dict(email="dev@gmail.com"))
    user_created_response = post(api_base_url, '/api/users', data=user_data)
    user_id = json.loads(user_created_response.content)['id']

    course_data = json.dumps(dict(name="Random Course"))
    course_created_response = post(api_base_url, '/api/courses', data=course_data)
    course_id = json.loads(course_created_response.content)['id']

    enroll_user_data = json.dumps(dict(user_id=user_id))
    user_enrolled_response = post(
        api_base_url,
        f'/api/courses/{course_id}/users',
        data=enroll_user_data,
    )

    uow = SqlAlchemyUnitOfWork(session_factory=postgres_session_factory)

    with uow:
        user = uow.users.get(user_id)
        course = uow.courses.get(course_id)

    assert user.id == user_id
    assert user.email == 'dev@gmail.com'
    assert course.id == course_id
    assert course.name == 'Random Course'
    assert course.is_enrolled(user)

    assert user_enrolled_response.status_code == 201
    assert json.loads(user_enrolled_response.content) == dict(
        course_id=course_id,
        user_id=user_id
    )

    enrollment_withdrawn_response = requests.delete(
        f'{api_base_url}/api/courses/{course_id}/users/{user_id}'
    )

    with uow:
        course = uow.courses.get(course_id)

    assert list(course.enrollments) == []
    assert enrollment_withdrawn_response.status_code == 204
