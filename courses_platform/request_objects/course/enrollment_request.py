from typing import Type, Union

from courses_platform.request_objects import InvalidRequest
from courses_platform.request_objects.valid_request import ValidRequest, VR


class EnrollmentRequest(ValidRequest):
    required_params = [
        'course_id',
        'user_id'
    ]

    def __init__(self, course_id: str, user_id: str) -> None:
        self.course_id = course_id
        self.user_id = user_id

    @classmethod
    def from_dict(cls: Type[VR], params: dict) -> Union[InvalidRequest, VR]:
        invalid_req = InvalidRequest()

        for required_param in cls.required_params:
            if required_param not in params:
                invalid_req.add_error(
                    required_param,
                    f'{required_param} is a required parameter'
                )

        if invalid_req.has_errors():
            return invalid_req

        return cls(
            course_id=params['course_id'],
            user_id=params['user_id']
        )
