from typing import Type, Union

from courses_platform.request_objects import InvalidRequest
from courses_platform.request_objects.valid_request import ValidRequest, VR


class CreateUserRequest(ValidRequest):
    def __init__(self, email: str) -> None:
        self.email = email

    @classmethod
    def from_dict(cls: Type[VR], params: dict) -> Union[InvalidRequest, VR]:
        invalid_req = InvalidRequest()

        if 'email' not in params:
            invalid_req.add_error('email', 'email is a required parameter')
            return invalid_req

        if not isinstance(params['email'], str):
            invalid_req.add_error('email', 'is not a string')
            return invalid_req

        return cls(email=params['email'])
