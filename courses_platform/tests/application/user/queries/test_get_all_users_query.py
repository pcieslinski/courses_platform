from app.domain.user import User
from app.response_objects import ResponseSuccess
from app.application.user.queries.get_all import GetAllUsersQuery


class TestGetAllUsersQuery:

    def test_get_all_users_query_returns_list_of_users(self, uow):
        with uow:
            user_1 = User(id='1', email='test@gmail.com')
            user_2 = User(id='2', email='dev@gmail.com')

            uow.users.add(user_1)
            uow.users.add(user_2)

        query = GetAllUsersQuery(unit_of_work=uow)
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
