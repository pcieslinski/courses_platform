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


class QuerySchema(ma.Schema):
    include = fields.List(fields.Str())


query_serializer = QuerySchema()
