import json


class UserJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                'id': o.id,
                'email': o.email
            }
            return to_serialize
        except AttributeError:
            super().default(o)
