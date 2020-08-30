# Courses Platform 📝

## Aproach 💡
The project includes a REST API that has been implemented in 
accordance with clean architecture. Leonardo Giordani's work 
inspired me very much during the development of this 
application. Especially I mean his book, which can be found 
[here](https://leanpub.com/clean-architectures-in-python).
Excellent book with very good examples, I highly recommend it.

The second source that is definitely worth mentioning here is 
the repository/book [CosmicPython](https://github.com/cosmicpython/book) 📘.

## Quickstart 📜
The fastest way to start an application is to use the `Makefile`. Run this command in
project root directory.

```bash
make build
make up
```

To add the startup data to the database, just use this command: 

```bash
make seed-db
```

To turn everything off:

```bash
make down
```

To run all tests, use this command:

```bash
make test
```

## Layers 🔬

```
app
├── __init__.py
├── adapters
│   ├── __init__.py
│   ├── orm.py
│   ├── repositories.py
│   └── unit_of_work.py
├── application
│   ├── __init__.py
│   ├── course
│   │   ├── __init__.py
│   │   ├── commands.py
│   │   └── queries.py
│   ├── user
│   │   ├── __init__.py
│   │   ├── commands.py
│   │   └── queries.py
│   ├── interfaces
│   │   ├── __init__.py
│   │   └── iunit_of_work.py
│   └── exceptions.py
├── domain
│   ├── __init__.py
│   ├── course.py
│   └── user.py
├── response_objects
│   ├── __init__.py
│   └── responses.py
└── service
    ├── __init__.py
    ├── config.py
    ├── course
    │   ├── __init__.py
    │   ├── serializers.py
    │   └── views.py
    ├── user
    │   ├── __init__.py
    │   ├── serializers.py
    │   └── views.py
    ├── extensions.py
    ├── parser.py
    ├── schemas.py
    └── status_codes.py
```

#### Domain
____________________
At the domain layer, two entities have been implemented: 
`User` and `Course`.
\
As you might expect, one user can be enrolled in many 
courses and courses can also have many different users.

#### Application
____________________
All functionalities have been broken down into a number of 
independent commands and queries.

#### Adapters
____________________
The adapters that have been implemented are mainly Repository
for interacting with the database and mapping objects from the
database to domain objects. Additionally, the Unit of Work pattern
was used here to ensure transactionality.

#### Service
____________________
The REST API was made with the very popular Flask micro-framework. 
It is very minimalistic and is based primarily on the application layer.

#### Error Management
____________________
Errors are raised in the application layer in specific commands and 
queries - this is where business rules can determine what the error really is.


## Endpoints 🚀

One of the best methods for testing the APIs is [HTTPie](https://httpie.org/). 
In this section, I will use commands using exactly this CLI.


### User


#### **/api/users**
____________________

`GET` - get a list of all users.

```bash
http :5000/api/users
```
```bash
http :5000/api/users include==courses
```
\
`POST` - create new user.
```bash
http POST :5000/api/users email='test@gmail.com'
```
  

#### **/api/users/<user_id>**
____________________

`GET` - get details of a specific user.
```bash
http :5000/api/users/123 
```
```bash
http :5000/api/users/123 include==courses
```
**Sample response**:

```json
{
    "_links": {
        "collection": "/api/users",
        "courses": "/api/users/4aa841d3-a852-408e-bd3f-e23b726b8d1a/courses",
        "self": "/api/users/4aa841d3-a852-408e-bd3f-e23b726b8d1a"
    },
    "courses": [
        {
            "_links": {
                "collection": "/api/courses",
                "enroll_user": "/api/courses/3ad9b870-b752-4854-9708-4fc6b703c64d/users",
                "self": "/api/courses/3ad9b870-b752-4854-9708-4fc6b703c64d"
            },
            "id": "3ad9b870-b752-4854-9708-4fc6b703c64d",
            "name": "Test Course"
        },
        {
            "_links": {
                "collection": "/api/courses",
                "enroll_user": "/api/courses/b39fefaa-a143-475c-9b4d-751b0843aaa8/users",
                "self": "/api/courses/b39fefaa-a143-475c-9b4d-751b0843aaa8"
            },
            "id": "b39fefaa-a143-475c-9b4d-751b0843aaa8",
            "name": "Sample Course"
        }
    ],
    "email": "sample@gmail.com",
    "id": "4aa841d3-a852-408e-bd3f-e23b726b8d1a"
}
```

\
`DELETE` - delete user.
```bash
http DELETE :5000/api/users/123 
```

#### **/api/users/<user_id>/courses**
____________________
`GET` - get a list of courses for a specific user.

```bash
http :5000/api/users/123/courses
```

### Course

#### **/api/courses/**
____________________
`GET` - get a list of all courses.

```bash
http :5000/api/courses
```
```bash
http :5000/api/courses include==enrollments
```
\
`POST` - create new course.

```bash
http POST :5000/api/courses name='Test Course'
```

#### **/api/courses/<course_id>**
____________________
`GET` - get details of a specific course.

```bash
http :5000/api/courses/123
```
```bash
http :5000/api/courses/123 include==enrollments
```

**Sample response**:
```json
{
    "_links": {
        "collection": "/api/courses",
        "enroll_user": "/api/courses/3ad9b870-b752-4854-9708-4fc6b703c64d/users",
        "self": "/api/courses/3ad9b870-b752-4854-9708-4fc6b703c64d"
    },
    "enrollments": [
        {
            "_links": {
                "collection": "/api/users",
                "courses": "/api/users/9c2f4dee-8db5-4045-95bb-c487d6d52e5b/courses",
                "self": "/api/users/9c2f4dee-8db5-4045-95bb-c487d6d52e5b"
            },
            "email": "test@gmail.com",
            "id": "9c2f4dee-8db5-4045-95bb-c487d6d52e5b"
        },
        {
            "_links": {
                "collection": "/api/users",
                "courses": "/api/users/4aa841d3-a852-408e-bd3f-e23b726b8d1a/courses",
                "self": "/api/users/4aa841d3-a852-408e-bd3f-e23b726b8d1a"
            },
            "email": "sample@gmail.com",
            "id": "4aa841d3-a852-408e-bd3f-e23b726b8d1a"
        }
    ],
    "enrollments_count": 2,
    "id": "3ad9b870-b752-4854-9708-4fc6b703c64d",
    "name": "Test Course"
}
```
\
`DELETE` - delete course.

```bash
http DELETE :5000/api/courses/123
```

#### **/api/courses/<course_id>/users**
____________________
`POST` - enroll a user on the course.

```bash
http POST :5000/api/courses/123/users user_id=321
```

#### **/api/courses/<course_id>/users/<user_id>**
____________________
`DELETE` - withdraw a user enrollment from a course.

```bash
http DELETE :5000/api/courses/123/users/321
```

## TODO 🏆

1. Add authentication layer with JWT.
2. Implement OpenAPI specification.
3. Create a K8S setup.
4. Add NGINX as a rivers proxy to the architecture.
