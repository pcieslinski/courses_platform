from app.application.interfaces.iunit_of_work import IUnitOfWork
from app.response_objects import Response, ResponseFailure, ResponseSuccess


class GetAllCoursesQuery:
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def execute(self) -> Response:
        try:
            with self.unit_of_work as uow:
                result = uow.courses.list()

                return ResponseSuccess.build_response_success(result)

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
