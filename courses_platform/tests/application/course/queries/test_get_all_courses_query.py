from app.domain.course import Course
from app.response_objects import ResponseSuccess
from app.application.course.queries import GetAllCoursesQuery


class TestGetAllCoursesQuery:

    def test_get_all_courses_query_executes_correctly(self, uow):
        with uow:
            uow.courses.add(Course(id='1', name='Test Course'))
            uow.courses.add(Course(id='2', name='Sample Course'))

        query = GetAllCoursesQuery(unit_of_work=uow)
        response = query.execute()

        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK

        assert len(response.value) == 2
        assert response.value[0].id == '1'
        assert response.value[0].name == 'Test Course'
        assert response.value[1].id == '2'
        assert response.value[1].name == 'Sample Course'
