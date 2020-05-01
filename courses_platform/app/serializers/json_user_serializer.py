import json
from typing import Any, Dict

from app.domain.user import User


ResultJson = Dict[str, Any]


class UserJsonEncoder(json.JSONEncoder):
    def default(self, user: User) -> ResultJson:
        try:
            to_serialize: ResultJson = {
                'id': user.id,
                'email': user.email
            }

            return to_serialize
        except AttributeError:
            return super().default(user)
