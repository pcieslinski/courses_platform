from __future__ import annotations

from typing import Union

from app.request_objects.invalid_request import InvalidRequest


class ResponseFailure:
    RESOURCE_ERROR = 'ResourceError'
    SYSTEM_ERROR = 'SystemError'
    PARAMETERS_ERROR = 'ParametersError'

    def __init__(self, type: str, message: Union[Exception, str]) -> None:
        self.type = type
        self.message = self._format_message(message)

    def _format_message(self, msg: Union[Exception, str]) -> str:
        if isinstance(msg, Exception):
            return f'{msg.__class__.__name__}: {msg}'
        return msg

    @property
    def value(self) -> dict:
        return {
            'type': self.type,
            'message': self.message
        }

    def __bool__(self) -> bool:
        return False

    @classmethod
    def build_from_invalid_request(cls, invalid_request: InvalidRequest) -> ResponseFailure:
        message = "\n".join(
            [f"{err['parameter']}: {err['message']}"
             for err in invalid_request.errors]
        )
        return cls(cls.PARAMETERS_ERROR, message)

    @classmethod
    def build_resource_error(cls, message: Exception) -> ResponseFailure:
        return cls(cls.RESOURCE_ERROR, message)

    @classmethod
    def build_system_error(cls, message: Exception) -> ResponseFailure:
        return cls(cls.SYSTEM_ERROR, message)

    @classmethod
    def build_parameters_error(cls, message: Union[Exception, str]) -> ResponseFailure:
        return cls(cls.PARAMETERS_ERROR, message)
