from marshmallow import fields

from app.service.extensions import ma
from app.service.schemas import ModelSchema


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
            'CourseSchema',
            many=True,
            only=('id', 'name', '_links')
        )
    }


user_serializer = UserSchema()
users_serializer = UserSchema(many=True)
