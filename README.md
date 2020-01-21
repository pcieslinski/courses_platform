# Courses Platform

## Aproach
The project includes a REST API that has been implemented in 
accordance with clean architecture. Leonardo Giordani's work 
inspired me very much during the development of this 
application. Especially I mean his book, which can be found 
[here](https://leanpub.com/clean-architectures-in-python).
Excellent book with very good examples, I highly recommend it.

## Quickstart
The fastest way to launch the application is to use the 
docker-compose configuration. Run these command in the 
project root directory.

```bash
docker-compose build
docker-compose up -d
```

The application includes CLI, which allows you to add test 
data to the database. 

```bash
docker-compose exec courses_platform python manage.py seed-db
```

To turn everything off:

```bash
docker-compose down -v
```

## Layers

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

#### Persistence
____________________
PostgreSQL was used as the database. In this layer there are 
practically only database models and the popular client for 
relational databases in Python - SQLAlchemy.

#### Service
____________________
The REST API was made with the very popular Flask micro-framework. 
It is very minimalistic and is based primarily on the application layer.

#### Error Management
____________________
As suggested by Leonardo Giordani in his book, I used Requests and 
Responses to manage errors within the application. Errors are raised
in the application layer in specific commands and queries - this is
where business rules can determine what the error really is.



## Endpoints

One of the best methods for testing the APIs is [HTTPie](https://httpie.org/). 
In this section, I will use commands using exactly this CLI.


### User


#### **/api/users**
____________________

`GET` - get a list of all users.

```bash
http :5000/api/users
```
\
`POST` - create new user.
```bash
http POST :5000/api/users email='test'
```
  

#### **/api/users/<user_id>**
____________________

`GET` - get details of a specific user.
```bash
http :5000/api/users/123 
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
\
 `GET` `/api/courses?include=stats` - get a list of all courses with number of 
enrollments for each one.

```bash
http :5000/api/courses include==stats
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

## TODO

1. Implement hypermedia controls.
2. Write integration tests.
3. Implement a solution that allows composing commands and queries 
into more complex abstractions.
4. Add NGINX as a rivers proxy to the architecture.
