from typing import Tuple, Type, TypeVar

from courses_platform.request_objects.invalid_request import InvalidRequest


VR = TypeVar('VR', bound='ValidRequest')


class ValidRequest:
    required_params: Tuple[str] = ()
    accepted_params: Tuple[str] = ()

    @classmethod
    def validate_required_params(
            cls: Type[VR], invalid_req: InvalidRequest, params: dict) -> InvalidRequest:

        for required_param in cls.required_params:
            if required_param not in params:
                invalid_req.add_error(
                    required_param,
                    f'{required_param} is a required parameter'
                )
        return invalid_req

    @classmethod
    def validate_accepted_params(
            cls: Type[VR], invalid_req: InvalidRequest, params: dict) -> InvalidRequest:

        for param in params:
            if param not in cls.accepted_params:
                invalid_req.add_error(
                    param,
                    f'{param} is not an acceptable parameter'
                )

        return invalid_req

    @classmethod
    def from_dict(cls: Type[VR], params: dict) -> None:
        raise NotImplementedError

    def __bool__(self) -> bool:
        return True
