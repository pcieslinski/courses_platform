from marshmallow import fields

from app.service.extensions import ma
from app.service.schemas import ModelSchema
from app.service.user.serializers import UserSchema


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


course_serializer = CourseSchema()
courses_serializer = CourseSchema(many=True)
