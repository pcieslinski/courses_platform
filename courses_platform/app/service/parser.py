from typing import Dict

from marshmallow import Schema
from werkzeug.local import LocalProxy
from webargs.flaskparser import FlaskParser


class Parser(FlaskParser):
    VALUES_SEPARATOR = ','

    def load_querystring(self, req: LocalProxy, schema: Schema) -> Dict:
        return self._structure_args(req.args)

    def _structure_args(self, args: Dict) -> Dict:
        data = {}
        for k, v in args.items():
            data[k] = v.split(self.VALUES_SEPARATOR)

        return data


parser = Parser()
use_args = parser.use_args
use_kwargs = parser.use_kwargs
