from typing import Tuple, Type, Union

from courses_platform.request_objects import InvalidRequest
from courses_platform.request_objects.valid_request import ValidRequest, VR


class DeleteCourseRequest(ValidRequest):
    required_params: Tuple[str] = ('course_id',)

    def __init__(self, course_id: str) -> None:
        self.course_id = course_id

    @classmethod
    def from_dict(cls: Type[VR], params: dict) -> Union[InvalidRequest, VR]:
        invalid_req = cls.validate_required_params(
            invalid_req=InvalidRequest(),
            params=params
        )

        if invalid_req.has_errors():
            return invalid_req

        return cls(course_id=params['course_id'])
