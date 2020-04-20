from __future__ import annotations

from typing import Tuple, Union

from app.request_objects.valid_request import ValidRequest
from app.request_objects.invalid_request import InvalidRequest


class CreateCourseRequest(ValidRequest):
    required_params: Tuple[str] = ('name',)

    def __init__(self, name: str) -> None:
        self.name = name

    @classmethod
    def from_dict(cls, params: dict) -> Union[InvalidRequest, CreateCourseRequest]:
        invalid_req = cls.validate_required_params(
            invalid_req=InvalidRequest(),
            params=params
        )

        if invalid_req.has_errors():
            return invalid_req

        if not isinstance(params['name'], str):
            invalid_req.add_error('name', 'is not a string')
            return invalid_req

        return cls(name=params['name'])
