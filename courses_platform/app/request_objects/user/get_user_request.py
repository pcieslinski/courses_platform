from __future__ import annotations

from typing import Tuple, Union

from app.request_objects.valid_request import ValidRequest
from app.request_objects.invalid_request import InvalidRequest


class GetUserRequest(ValidRequest):
    required_params: Tuple[str] = ('user_id',)

    def __init__(self, user_id: str) -> None:
        self.user_id = user_id

    @classmethod
    def from_dict(cls, params: dict) -> Union[InvalidRequest, GetUserRequest]:
        invalid_req = cls.validate_required_params(
            invalid_req=InvalidRequest(),
            params=params
        )

        if invalid_req.has_errors():
            return invalid_req

        return cls(user_id=params['user_id'])
