from collections import namedtuple
from marshmallow import Schema
from sqlalchemy import Table
from sqlalchemy.sql import select, insert
from typing import Callable, List

from database import engine, meta

Job = namedtuple('Job', ['source', 'destination', 'schema'])

jobs: List[Job] = []


def transformation(source: str, destination: Table) -> Callable[[Schema], Schema]:
    def _decorate(cls: Schema) -> Schema:
        jobs.append(Job(
            source=source,
            destination=destination,
            schema=cls
        ))
        return cls
    return _decorate


def run() -> None:
    for job in jobs:
        source = Table(job.source, meta, autoload=True)
        schema = job.schema()

        with engine.connect() as c:
            result = c.execute(select([source]))
            data = result.fetchall()
            data = [schema.load(dict(d)) for d in data]
            # data = schema.load(data, many=True)
            query = job.destination.insert()
            c.execute(query, data)
