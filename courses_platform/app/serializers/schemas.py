from typing import Dict, List
from marshmallow import Schema, fields


class BaseSchema(Schema):
    includable_fields: Dict[str, fields.Field]

    def __init__(self, include: List[str] = None, **kwargs) -> None:
        super().__init__(**kwargs)

        fields = self.get_fields(include) if include else {}
        self.declared_fields.update(fields)
        self.dump_fields.update(fields)

    def get_fields(self, to_include: List[str]) -> Dict[str, fields.Field]:
        return {
            key: value
            for include in to_include
            for (key, value) in self.includable_fields.items()
            if include == key
        }


class UserSchema(BaseSchema):
    id = fields.Str()
    email = fields.Email()

    includable_fields = {
        'courses': fields.Nested(
            lambda: CourseSchema(
                many=True,
                only=('id', 'name')
            )
        )
    }


class CourseSchema(BaseSchema):
    id = fields.Str()
    name = fields.Str()

    includable_fields = {
        'enrollments': fields.Nested(
            UserSchema(
                many=True,
                only=('id', 'email')
            )
        ),
        'enrollments_count': fields.Integer()
    }
