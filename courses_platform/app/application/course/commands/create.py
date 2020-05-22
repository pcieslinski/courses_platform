from app.domain.course import Course
from app.application.interfaces.iunit_of_work import IUnitOfWork
from app.response_objects import Response, ResponseFailure, ResponseSuccess


class CreateCourseCommand:
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def execute(self, name: str) -> Response:
        try:
            with self.unit_of_work as uow:
                new_course = Course(name=name)
                uow.courses.add(new_course)

            return ResponseSuccess.build_response_resource_created(new_course)

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
