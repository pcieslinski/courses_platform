from typing import Tuple, Type, Union

from app.request_objects.invalid_request import InvalidRequest
from app.request_objects.valid_request import ValidRequest, VR


class EnrollmentRequest(ValidRequest):
    required_params: Tuple[str] = ('course_id', 'user_id')

    def __init__(self, course_id: str, user_id: str) -> None:
        self.course_id = course_id
        self.user_id = user_id

    @classmethod
    def from_dict(cls: Type[VR], params: dict) -> Union[InvalidRequest, VR]:
        invalid_req = cls.validate_required_params(
            invalid_req=InvalidRequest(),
            params=params
        )

        if invalid_req.has_errors():
            return invalid_req

        return cls(
            course_id=params['course_id'],
            user_id=params['user_id']
        )
