class NoMatchingCourse(Exception):
    def __init__(self, course_id: str) -> None:
        self.course_id = course_id

    def __str__(self) -> str:
        return f'No Course has been found for a given id: {self.course_id}'


class NoMatchingUser(Exception):
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id

    def __str__(self) -> str:
        return f'No User has been found for a given id: {self.user_id}'


class UserAlreadyEnrolled(Exception):
    def __init__(self, user_id: str, course_id: str) -> None:
        self.user_id = user_id
        self.course_id = course_id

    def __str__(self) -> str:
        return f'User: {self.user_id} is already enrolled in Course: {self.course_id}'


class UserNotEnrolled(Exception):
    def __init__(self, user_id: str, course_id: str) -> None:
        self.user_id = user_id
        self.course_id = course_id

    def __str__(self) -> str:
        return f'User: {self.user_id} is not enrolled in Course: {self.course_id}'


class UserAlreadyExists(Exception):
    def __init__(self, email: str) -> None:
        self.email = email

    def __str__(self) -> str:
        return f'User with "{self.email}" email already exists'
