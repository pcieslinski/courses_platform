from typing import Dict, List
from marshmallow import fields

from app.service.extensions import ma


class ModelSchema(ma.Schema):
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


class UserSchema(ModelSchema):
    id = fields.Str(dump_only=True)
    email = fields.Email(required=True)
    _links = ma.Hyperlinks(
        {
            'self': ma.URLFor('user_details', user_id='<id>'),
            'courses': ma.URLFor('user_courses', user_id='<id>'),
            'collection': ma.URLFor('users')
        }
    )

    includable_fields = {
        'courses': fields.Nested(
            lambda: CourseSchema(
                many=True,
                only=('id', 'name', '_links')
            )
        )
    }


class CourseSchema(ModelSchema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    enrollments_count = fields.Integer(dump_only=True)
    _links = ma.Hyperlinks(
        {
            'self': ma.URLFor('course_details', course_id='<id>'),
            'enroll_user': ma.URLFor('course_enrollment', course_id='<id>'),
            'collection': ma.URLFor('courses')
        }
    )

    includable_fields = {
        'enrollments': fields.Nested(
            UserSchema(
                many=True,
                only=('id', 'email', '_links')
            )
        )
    }


class QuerySchema(ma.Schema):
    include = fields.List(fields.Str())
