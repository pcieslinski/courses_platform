import json


class CourseJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                'id': o.id,
                'name': o.name
            }
            return to_serialize
        except AttributeError:
            super().default(o)
