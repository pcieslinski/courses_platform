from .schemas import UserSchema, CourseSchema, QuerySchema


user_serializer = UserSchema()
users_serializer = UserSchema(many=True)

course_serializer = CourseSchema()
courses_serializer = CourseSchema(many=True)

query_serializer = QuerySchema()
