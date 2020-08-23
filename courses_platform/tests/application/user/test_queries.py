import mock

from app.domain.user import User
from app.domain.course import Course
from app.application.user import queries
from app.response_objects import ResponseSuccess, ResponseFailure


class TestGetAllUsersQuery:

    def test_get_all_users_query_returns_list_of_users(self, uow):
        with uow:
            user_1 = User(id='1', email='test@gmail.com')
            user_2 = User(id='2', email='dev@gmail.com')

            uow.users.add(user_1)
            uow.users.add(user_2)

        query = queries.GetAllUsersQuery(unit_of_work=uow)
        response = query.execute()

        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK

        assert len(response.value) == 2
        assert response.value[0].id == '1'
        assert response.value[0].email == 'test@gmail.com'
        assert response.value[0].courses == []
        assert response.value[1].id == '2'
        assert response.value[1].email == 'dev@gmail.com'
        assert response.value[1].courses == []


class TestGetUserCoursesQuery:

    def test_get_user_courses_executes_correctly(self, uow):
        with uow:
            user = User(id='1',
                        email='test@gmail.com',
                        courses=[Course(id='100', name='Test Course')])

            uow.users.add(user)

        query = queries.GetUserCoursesQuery(unit_of_work=uow)
        response = query.execute(user_id='1')

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK
        assert len(response.value) == 1
        assert isinstance(response.value[0], Course)
        assert response.value[0].id == '100'
        assert response.value[0].name == 'Test Course'

    def test_get_user_courses_returns_resource_error(self, uow):
        query = queries.GetUserCoursesQuery(unit_of_work=uow)
        response = query.execute(user_id='1')

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingUser: No User has been found for a given id: 1'

    @mock.patch('app.adapters.unit_of_work.SqlAlchemyUnitOfWork')
    def test_get_user_courses_returns_system_error(self, mock_uow):
        session = mock.Mock()
        session.users.get.side_effect = Exception('System error.')
        mock_uow.__enter__.return_value = session

        query = queries.GetUserCoursesQuery(unit_of_work=mock_uow)
        response = query.execute(user_id='1')

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'


class TestGetUserQuery:

    def test_get_user_query_executes_correctly(self, uow):
        with uow:
            uow.users.add(User(id='100', email='test@gmail.com'))

        query = queries.GetUserQuery(unit_of_work=uow)
        response = query.execute(user_id='100')

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK
        assert response.value.email == 'test@gmail.com'
        assert response.value.courses == []

    def test_qet_user_query_returns_exception_when_no_resource_has_been_found(self, uow):
        query = queries.GetUserQuery(unit_of_work=uow)
        response = query.execute(user_id='100')

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingUser: No User has been found for a given id: 100'

    @mock.patch('app.adapters.unit_of_work.SqlAlchemyUnitOfWork')
    def test_get_user_query_returns_system_error_when_generic_exception_is_raised(self, mock_uow):
        session = mock.Mock()
        session.users.get.side_effect = Exception('System error.')
        mock_uow.__enter__.return_value = session

        query = queries.GetUserQuery(unit_of_work=mock_uow)
        response = query.execute(user_id='100')

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'
