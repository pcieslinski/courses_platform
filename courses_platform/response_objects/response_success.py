from typing import Any, Type, TypeVar


RS = TypeVar('RS', bound='ResponseSuccess')


class ResponseSuccess:
    SUCCESS_OK = 'Success'
    SUCCESS_RESOURCE_CREATED = 'SuccessResourceCreated'
    SUCCESS_NO_CONTENT = 'SuccessNoContent'

    def __init__(self, type: str, value: Any = None) -> None:
        self.type = type
        self.value = value

    def __bool__(self) -> bool:
        return True

    @classmethod
    def build_response_success(cls: Type[RS], value: Any) -> RS:
        return cls(cls.SUCCESS_OK, value)

    @classmethod
    def build_response_resource_created(cls: Type[RS], value: Any) -> RS:
        return cls(cls.SUCCESS_RESOURCE_CREATED, value)

    @classmethod
    def build_response_no_content(cls: Type[RS], value: Any = '') -> RS:
        return cls(cls.SUCCESS_NO_CONTENT, value)
