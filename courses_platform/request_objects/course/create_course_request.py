from typing import Tuple, Type, Union

from courses_platform.request_objects import InvalidRequest
from courses_platform.request_objects.valid_request import ValidRequest, VR


class CreateCourseRequest(ValidRequest):
    required_params: Tuple[str] = ('name',)

    def __init__(self, name: str) -> None:
        self.name = name

    @classmethod
    def from_dict(cls: Type[VR], params: dict) -> Union[InvalidRequest, VR]:
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
