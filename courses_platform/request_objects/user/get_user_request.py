from typing import Type, Union

from courses_platform.request_objects import InvalidRequest
from courses_platform.request_objects.valid_request import ValidRequest, VR


class GetUserRequest(ValidRequest):
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id

    @classmethod
    def from_dict(cls: Type[VR], params: dict) -> Union[InvalidRequest, VR]:
        invalid_req = InvalidRequest()

        if 'user_id' not in params:
            invalid_req.add_error('user_id', 'user_id is a required parameter')
            return invalid_req

        return cls(user_id=params['user_id'])
