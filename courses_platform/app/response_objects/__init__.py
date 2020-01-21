from typing import NewType, Union

from app.response_objects.response_failure import ResponseFailure
from app.response_objects.response_success import ResponseSuccess

Response = NewType('Response', Union[ResponseFailure, ResponseSuccess])
