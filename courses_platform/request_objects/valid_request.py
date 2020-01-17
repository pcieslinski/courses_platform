from typing import Type, TypeVar


VR = TypeVar('VR', bound='ValidRequest')


class ValidRequest:
    @classmethod
    def from_dict(cls: Type[VR], params: dict) -> None:
        raise NotImplementedError

    def __bool__(self) -> bool:
        return True
