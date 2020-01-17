from typing import NewType, Union

from courses_platform.response_objects.response_failure import ResponseFailure
from courses_platform.response_objects.response_success import ResponseSuccess

Response = NewType('Response', Union[ResponseFailure, ResponseSuccess])
