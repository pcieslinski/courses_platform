from typing import Union

from app.application.interfaces.iunit_of_work import IUnitOfWork
from app.application.interfaces.icommand_query import ICommandQuery

from app.request_objects.valid_request import ValidRequest
from app.request_objects.invalid_request import InvalidRequest
from app.response_objects import Response, ResponseFailure, ResponseSuccess


Request = Union[InvalidRequest, ValidRequest]


class GetAllUsersQuery(ICommandQuery):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def execute(self, request: Request = None) -> Response:
        try:
            with self.unit_of_work as uow:
                result = uow.users.list()

                return ResponseSuccess.build_response_success(result)

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
