import json


class UserJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                'id': o.id,
                'email': o.email
            }

            if hasattr(o, 'courses'):
                to_serialize['courses'] = [
                    course.__dict__
                    for course in o.courses
                ]

            return to_serialize
        except AttributeError:
            super().default(o)
