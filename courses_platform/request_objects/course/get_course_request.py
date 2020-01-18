from typing import Type, Union

from courses_platform.request_objects import InvalidRequest
from courses_platform.request_objects.valid_request import ValidRequest, VR


class GetCourseRequest(ValidRequest):
    def __init__(self, course_id: str) -> None:
        self.course_id = course_id

    @classmethod
    def from_dict(cls: Type[VR], params: dict) -> Union[InvalidRequest, VR]:
        invalid_req = InvalidRequest()

        if 'course_id' not in params:
            invalid_req.add_error('course_id', 'course_id is a required parameter')
            return invalid_req

        return cls(course_id=params['course_id'])
