from typing import Dict


def generate_course_links(course_id: str) -> Dict:
    return {
        'self': f'/api/courses/{course_id}',
        'enroll_user': f'/api/courses/{course_id}/users',
        'collection': '/api/courses'
    }


def generate_user_links(user_id: str) -> Dict:
    return {
        'self': f'/api/users/{user_id}',
        'courses': f'/api/users/{user_id}/courses',
        'collection': '/api/users'
    }
