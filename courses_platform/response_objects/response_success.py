from typing import Any


class ResponseSuccess:
    SUCCESS = 'Success'

    def __init__(self, value: Any = None) -> None:
        self.type = self.SUCCESS
        self.value = value

    def __bool__(self) -> bool:
        return True
