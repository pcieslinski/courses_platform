import yaml
from apispec import APISpec

OPENAPI_SPEC = """
openapi: 3.0.2
info:
  description: Course Platform API Documentation
  title: Course Platform API
  version: 1.0.0
servers:
- url: http://localhost:{port}/
  description: The development API server
  variables:
    port:
      enum:
      - '3000'
      - '8888'
      default: '3000'
"""

settings = yaml.safe_load(OPENAPI_SPEC)
title = settings["info"].pop("title")
spec_version = settings["info"].pop("version")
openapi_version = settings.pop("openapi")

spec = APISpec(
    title=title,
    version=spec_version,
    openapi_version=openapi_version,
    **settings
)

spec.components.schema(
    'User',
    {
        'properties': {
            'id': {'type': 'string'},
            'email': {
                'type': 'string',
                'format': 'email'
            },
            '_links': {
                'type': 'object',
                'properties': {
                    'self': {'type': 'uri'},
                    'courses': {'type': 'uri'},
                    'collection': {'type': 'uri'}
                }
            },
        }
    }
)

spec.components.schema(
    'Course',
    {
        'properties': {
            'id': {'type': 'string'},
            'name': {'type': 'string'},
            'enrollments_count': {
                'type': 'integer',
                'format': 'int64'
            },
            '_links': {
                'type': 'object',
                'properties': {
                    'self': {'type': 'uri'},
                    'enroll_user': {'type': 'uri'},
                    'collection': {'type': 'uri'}
                }
            },
        }
    }
)
