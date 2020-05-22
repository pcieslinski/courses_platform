import mock

from app.domain.user import User
from app.domain.course import Course
from app.response_objects import ResponseSuccess, ResponseFailure
from app.application.user.queries.get_user_courses import GetUserCoursesQuery


class TestGetUserCoursesQuery:

    def test_get_user_courses_executes_correctly(self, uow):
        with uow:
            user = User(id='1',
                        email='test@gmail.com',
                        courses=[Course(id='100', name='Test Course')])

            uow.users.add(user)

        query = GetUserCoursesQuery(unit_of_work=uow)
        response = query.execute(user_id='1')

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK
        assert len(response.value) == 1
        assert isinstance(response.value[0], Course)
        assert response.value[0].id == '100'
        assert response.value[0].name == 'Test Course'

    def test_get_user_courses_returns_resource_error(self, uow):
        query = GetUserCoursesQuery(unit_of_work=uow)
        response = query.execute(user_id='1')

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingUser: No User has been found for a given id: 1'

    @mock.patch('app.persistence.unit_of_work.SqlAlchemyUnitOfWork')
    def test_get_user_courses_returns_system_error(self, mock_uow):
        session = mock.Mock()
        session.users.get.side_effect = Exception('System error.')
        mock_uow.__enter__.return_value = session

        query = GetUserCoursesQuery(unit_of_work=mock_uow)
        response = query.execute(user_id='1')

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'
