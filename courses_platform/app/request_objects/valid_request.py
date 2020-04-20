from __future__ import annotations

import abc
from typing import Sequence, Union

from app.request_objects.invalid_request import InvalidRequest


class ValidRequest(abc.ABC):
    required_params: Sequence[str] = ()
    accepted_params: Sequence[str] = ()

    @classmethod
    def validate_required_params(
            cls, invalid_req: InvalidRequest, params: dict) -> InvalidRequest:

        for required_param in cls.required_params:
            if required_param not in params:
                invalid_req.add_error(
                    required_param,
                    f'{required_param} is a required parameter'
                )
        return invalid_req

    @classmethod
    def validate_accepted_params(
            cls, invalid_req: InvalidRequest, params: dict) -> InvalidRequest:

        for param in params:
            if param not in cls.accepted_params:
                invalid_req.add_error(
                    param,
                    f'{param} is not an acceptable parameter'
                )

        return invalid_req

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, params: dict) -> Union[InvalidRequest, ValidRequest]:
        raise NotImplementedError
