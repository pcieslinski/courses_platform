from __future__ import annotations

from typing import Tuple, Union

from app.request_objects.valid_request import ValidRequest
from app.request_objects.invalid_request import InvalidRequest


class DeleteCourseRequest(ValidRequest):
    required_params: Tuple[str] = ('course_id',)

    def __init__(self, course_id: str) -> None:
        self.course_id = course_id

    @classmethod
    def from_dict(cls, params: dict) -> Union[InvalidRequest, DeleteCourseRequest]:
        invalid_req = cls.validate_required_params(
            invalid_req=InvalidRequest(),
            params=params
        )

        if invalid_req.has_errors():
            return invalid_req

        return cls(course_id=params['course_id'])
