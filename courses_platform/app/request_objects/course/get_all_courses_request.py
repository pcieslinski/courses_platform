from __future__ import annotations

from typing import List, Tuple, Union

from app.request_objects.valid_request import ValidRequest
from app.request_objects.invalid_request import InvalidRequest


class GetAllCoursesRequest(ValidRequest):
    accepted_params: Tuple[str] = ('include',)
    accepted_include_values: Tuple[str] = ('enrollments_count',)

    def __init__(self, include: List[str] = None) -> None:
        self.include = include or []

    @staticmethod
    def split_include(include: str) -> List[str]:
        return include.split(',')

    @classmethod
    def from_dict(cls, params: dict) -> Union[InvalidRequest, GetAllCoursesRequest]:
        invalid_req = cls.validate_accepted_params(
            invalid_req=InvalidRequest(),
            params=params
        )

        if 'include' in params:
            params['include'] = cls.split_include(params['include'])

            for param in params['include']:
                if param not in cls.accepted_include_values:
                    invalid_req.add_error(
                        param,
                        f'{param} cannot be included with Courses'
                    )

        if invalid_req.has_errors():
            return invalid_req

        return cls(include=params.get('include', None))
