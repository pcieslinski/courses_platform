import json


class UserJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                'id': o.id,
                'email': o.email,
                'courses': [c.__dict__ for c in o.courses]
            }
            return to_serialize
        except AttributeError:
            super().default(o)
