from typing import Union

from sqlalchemy.exc import IntegrityError

from app.request_objects.invalid_request import InvalidRequest
from app.request_objects.user.create_user_request import CreateUserRequest
from app.response_objects import Response, ResponseFailure, ResponseSuccess

from app.domain.user import User
from app.application.user.exceptions import UserAlreadyExists
from app.application.interfaces.iunit_of_work import IUnitOfWork
from app.application.interfaces.icommand_query import ICommandQuery


Request = Union[CreateUserRequest, InvalidRequest]


class CreateUserCommand(ICommandQuery):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def execute(self, request: Request) -> Response:
        if isinstance(request, InvalidRequest):
            return ResponseFailure.build_from_invalid_request(request)

        try:
            with self.unit_of_work as uow:
                new_user = User(email=request.email)
                uow.users.add(new_user)

            return ResponseSuccess.build_response_resource_created(new_user)

        except IntegrityError:
            return ResponseFailure.build_resource_error(
                UserAlreadyExists(
                    f'User with "{new_user.email}" email already exists.'
                ))

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
