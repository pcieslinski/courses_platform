from __future__ import annotations
import abc
import json
from typing import Any, Union

from marshmallow import Schema


class ResponseBase(abc.ABC):
    type: str
    value: Any

    @abc.abstractmethod
    def __bool__(self) -> bool:
        raise NotImplementedError

    def serialize(self, schema: Schema = None) -> str:
        return schema.dumps(self.value) if schema else json.dumps(self.value)


class ResponseSuccess(ResponseBase):
    """
    Wrapper for all successful application layer responses.

    Args:
        - type (str): One of the three types of successful responses: `Success`,
            `SuccessResourceCreated`, `SuccessNoContent`
        - value (Any, optional): The value that is returned by the application layer
    """

    SUCCESS_OK = 'Success'
    SUCCESS_RESOURCE_CREATED = 'SuccessResourceCreated'
    SUCCESS_NO_CONTENT = 'SuccessNoContent'

    def __init__(self, type: str, value: Any = None) -> None:
        self.type = type
        self.value = value

    def __bool__(self) -> bool:
        return True

    @classmethod
    def build_response_success(cls, value: Any) -> ResponseSuccess:
        return cls(cls.SUCCESS_OK, value)

    @classmethod
    def build_response_resource_created(cls, value: Any) -> ResponseSuccess:
        return cls(cls.SUCCESS_RESOURCE_CREATED, value)

    @classmethod
    def build_response_no_content(cls, value: Any = '') -> ResponseSuccess:
        return cls(cls.SUCCESS_NO_CONTENT, value)


class ResponseFailure(ResponseBase):
    """
    Wrapper for all failed responses from the application layer.

    Args:
        - type (str): One of the three types of failed responses: `ResourceError`, `SystemError`
        - message (Union[Exception, str]): The message that is passed from the application layer
            can either be an Exception, in which case the traceback will be used to build the message,
            or a regular string.
    """

    RESOURCE_ERROR = 'ResourceError'
    SYSTEM_ERROR = 'SystemError'

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
    def build_resource_error(cls, message: Exception) -> ResponseFailure:
        return cls(cls.RESOURCE_ERROR, message)

    @classmethod
    def build_system_error(cls, message: Exception) -> ResponseFailure:
        return cls(cls.SYSTEM_ERROR, message)
