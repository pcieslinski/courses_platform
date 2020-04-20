from typing import Union

from app.response_objects.response_failure import ResponseFailure
from app.response_objects.response_success import ResponseSuccess

Response = Union[ResponseFailure, ResponseSuccess]
