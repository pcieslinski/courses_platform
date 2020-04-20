from typing import List, Dict


class InvalidRequest:
    def __init__(self) -> None:
        self.errors: List[Dict] = []

    def add_error(self, parameter: str, message: str) -> None:
        self.errors.append(
            {
                'parameter': parameter,
                'message': message
            }
        )

    def has_errors(self) -> bool:
        return len(self.errors) > 0
