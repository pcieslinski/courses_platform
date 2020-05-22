from app.application import exceptions as ex
from app.application.interfaces.iunit_of_work import IUnitOfWork
from app.response_objects import Response, ResponseFailure, ResponseSuccess


class GetCourseQuery:
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def execute(self, course_id: str) -> Response:
        try:
            with self.unit_of_work as uow:
                course = uow.courses.get(course_id)

                if not course:
                    return ResponseFailure.build_resource_error(
                        ex.NoMatchingCourse(course_id)
                    )

                return ResponseSuccess.build_response_success(course)

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
