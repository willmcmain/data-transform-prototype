from collections import namedtuple
from marshmallow import Schema
from sqlalchemy import Table
from sqlalchemy.sql import select, insert
from typing import Callable, List

from .database import engine, meta
from .custom_fields import RelatedMany

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
        many_fields = []
        for field_name, field in schema._declared_fields.items():
            if isinstance(field, RelatedMany):
                many_fields.append(field_name)

        with engine.connect() as c:
            result = c.execute(select([source]))
            data = result.fetchall()
            data = schema.load((dict(d) for d in data), many=True)
            query = job.destination.insert()
            c.execute(query, data)
            # handle many to many relationships
            for datum in data:
                for field_name in many_fields:
                    bridge_job = datum[field_name]
                    for uuid in bridge_job.uuids:
                        select_query = (select([job.destination.c.id, bridge_job.related.c.id])
                            .where((job.destination.c.uuid == datum['uuid'])
                                & (bridge_job.related.c.uuid.in_(datum[field_name].uuids)) ))
                        query = (bridge_job.bridge.insert().from_select(
                            [bridge_job.source_column, bridge_job.destination_column], select_query))
                            
                        c.execute(query)


# from sqlalchemy.sql import table, column
# >>> t1 = table('t1', column('a'), column('b'))
# >>> t2 = table('t2', column('x'), column('y'))
# >>> print(t1.insert().from_select(['a', 'b'], t2.select().where(t2.c.y == 5)))