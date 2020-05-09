import pytest

from app.domain.user import User
from app.domain.course import Course
from app.response_objects import ResponseSuccess
from app.request_objects.course import GetAllCoursesRequest
from app.persistence.unit_of_work import SqlAlchemyUnitOfWork
from app.application.course.queries.get_all import GetAllCoursesQuery


@pytest.fixture
def uow(session_factory) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory)


class TestGetAllCoursesQuery:

    def test_get_all_courses_query_executes_correctly(self, uow):
        with uow:
            uow.courses.add(Course(id='1', name='Test Course'))
            uow.courses.add(Course(id='2', name='Sample Course'))

        query = GetAllCoursesQuery(unit_of_work=uow)
        response = query.execute(request=GetAllCoursesRequest())

        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK

        assert len(response.value) == 2
        assert response.value[0].id == '1'
        assert response.value[0].name == 'Test Course'
        assert response.value[1].id == '2'
        assert response.value[1].name == 'Sample Course'

    def test_get_all_courses_query_returns_courses_with_stats(self, uow):
        with uow:
            user = User(id='25', email='test@gmail.com')
            course = Course(id='10', name='Test Course')

            course.enrollments.append(user)

            uow.users.add(user)
            uow.courses.add(course)

        query = GetAllCoursesQuery(unit_of_work=uow)
        response = query.execute(request=GetAllCoursesRequest(include=['stats']))

        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK

        assert len(response.value) == 1
        assert response.value[0]['course'].id == '10'
        assert response.value[0]['course'].name == 'Test Course'
        assert response.value[0]['enrollments'] == 1
