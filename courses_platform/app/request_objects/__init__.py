from typing import NewType, Union

from app.request_objects.valid_request import ValidRequest
from app.request_objects.invalid_request import InvalidRequest

Request = NewType('Request', Union[ValidRequest, InvalidRequest])

