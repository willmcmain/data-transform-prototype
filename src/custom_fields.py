from collections import namedtuple
from marshmallow import fields
from sqlalchemy import Table
from sqlalchemy.sql import select

from . import database

class Related(fields.Field):
    def __init__(self, table):
        super().__init__()
        self.table = table

    def __repr__(self):
        return "Related"

    def _deserialize(self, value, attr, data, **kwargs):
        query = select([self.table.c.id]).where(
            self.table.c.uuid == value)
        with database.engine.connect() as c:
            result = c.execute(query)
            return result.fetchone().id


class RelatedMany(fields.Field):
    def __init__(self, related: Table, bridge: Table, source_column: str, destination_column: str):
        super().__init__()
        self.related = related
        self.bridge = bridge
        self.source_column = source_column
        self.destination_column = destination_column 

    def __repr__(self):
        return "RelatedMany"

    def _deserialize(self, value, attr, data, **kwargs):
        return RelatedJob(related=self.related, bridge=self.bridge, uuids=value,
            source_column=self.source_column, destination_column=self.destination_column)

class RelatedSelf(field.Field):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "RelatedSelf"

    def _deserialize(self, value, attr, data, **kwargs):
        



RelatedJob = namedtuple('RelatedJob', ['related', 'bridge', 'uuids', 'source_column', 'destination_column'])