from typing import Union

from app.response_objects.responses import ResponseFailure, ResponseSuccess

Response = Union[ResponseFailure, ResponseSuccess]
