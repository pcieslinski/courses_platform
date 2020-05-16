from .schemas import UserSchema, CourseSchema


user_serializer = UserSchema()
users_serializer = UserSchema(many=True)
course_serializer = CourseSchema()
courses_serializer = CourseSchema(many=True)
