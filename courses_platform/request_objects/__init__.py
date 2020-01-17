from typing import NewType, Union

from courses_platform.request_objects.valid_request import ValidRequest
from courses_platform.request_objects.invalid_request import InvalidRequest

Request = NewType('Request', Union[ValidRequest, InvalidRequest])

