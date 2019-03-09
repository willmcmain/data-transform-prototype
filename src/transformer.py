from marshmallow import Schema
from typing import Callable


def transformation(source: str, destination: str) -> Callable[[Schema], Schema]:
    def _decorate(cls: Schema) -> Schema:
        return cls
    return _decorate
