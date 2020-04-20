from __future__ import annotations

from typing import Tuple, Union

from app.request_objects.valid_request import ValidRequest
from app.request_objects.invalid_request import InvalidRequest


class CreateUserRequest(ValidRequest):
    required_params: Tuple[str] = ('email',)

    def __init__(self, email: str) -> None:
        self.email = email

    @classmethod
    def from_dict(cls, params: dict) -> Union[InvalidRequest, CreateUserRequest]:
        invalid_req = cls.validate_required_params(
            invalid_req=InvalidRequest(),
            params=params
        )

        if invalid_req.has_errors():
            return invalid_req

        if not isinstance(params['email'], str):
            invalid_req.add_error('email', 'is not a string')
            return invalid_req

        return cls(email=params['email'])
