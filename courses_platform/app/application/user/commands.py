from typing import cast

from sqlalchemy.exc import IntegrityError

from app.domain.user import User
from app.application import exceptions as ex
from app.application.interfaces.iunit_of_work import IUnitOfWork
from app.response_objects import Response, ResponseFailure, ResponseSuccess


class CreateUserCommand:
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def execute(self, email: str) -> Response:
        try:
            with self.unit_of_work as uow:
                new_user = User(email=email)
                uow.users.add(new_user)

            return ResponseSuccess.build_response_resource_created(new_user)

        except IntegrityError:
            return ResponseFailure.build_resource_error(
                ex.UserAlreadyExists(new_user.email)
            )

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)


class DeleteUserCommand:
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def execute(self, user_id: str) -> Response:
        try:
            with self.unit_of_work as uow:
                user = cast(User, uow.users.get(user_id))

                if user:
                    user.clear_enrollments()
                    uow.users.remove(user)
                else:
                    return ResponseFailure.build_resource_error(
                        ex.NoMatchingUser(user_id)
                    )

            return ResponseSuccess.build_response_no_content()

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
