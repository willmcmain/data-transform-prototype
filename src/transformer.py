from collections import namedtuple, defaultdict
from marshmallow import Schema
from sqlalchemy import Table
from sqlalchemy.sql import select, insert
from typing import Callable, List

from .database import engine, meta
from .custom_fields import RelatedMany, Related, RelatedSelf

Job = namedtuple('Job', ['source', 'destination', 'schema'])

jobs = {}


def topological_sort_jobs(job_graph):
    """Generate a sorted list of jobs from a dependency graph

    Node shape:
        'table_name':{
            'dependencies': ['list of dependencies'] or None,
            'job': ActualJobObject
        }
    """
    visited = defaultdict(bool)
    visited_temp = defaultdict(bool)
    job_list = []
    
    def search_dependencies(node, job_graph):
        if visited[node]:
            return
        if visited_temp[node]:
            raise ValueError("Cycle detected")
        dependencies = job_graph[node]['dependencies']
        job = job_graph[node]['job']
        visited_temp[node] = True
        if dependencies:
            for dependency in dependencies:
                search_dependencies(dependency, job_graph)
        job_list.append(job)
        visited[node] = True

    for node in job_graph:
        search_dependencies(node, job_graph)
    
    return job_list


def transformation(source: str, destination: Table) -> Callable[[Schema], Schema]:
    def _decorate(cls: Schema) -> Schema:
        job = Job(
            source=source,
            destination=destination,
            schema=cls
        )
        dependencies = []
        for field_name, field in cls._declared_fields.items():
            if isinstance(field, RelatedMany):
                dependencies.append(field.related.name)
            
            if isinstance(field, Related):
                dependencies.append(field.table.name)

        jobs[destination.name] = {
            'job': job,
            'dependencies': dependencies or None
        }

        return cls
    return _decorate


def run() -> None:
    # sort jobs here
    for job in topological_sort_jobs(jobs):
        source = Table(job.source, meta, autoload=True)
        schema = job.schema()
        many_fields = []
        self_fields = []
        for field_name, field in schema._declared_fields.items():
            if isinstance(field, RelatedMany):
                many_fields.append(field_name)
            if isinstance(field, RelatedSelf):
                self_fields.append(field_name)

        with engine.connect() as c:
            result = c.execute(select([source]))
            data = result.fetchall()
            data = schema.load((dict(d) for d in data), many=True)
            query = job.destination.insert()
            c.execute(query, data)
            for datum in data:
                # handle many to many relationships
                for field_name in many_fields:
                    bridge_job = datum[field_name]
                    select_query = (select([job.destination.c.id, bridge_job.related.c.id])
                        .where((job.destination.c.uuid == datum['uuid'])
                            & (bridge_job.related.c.uuid.in_(bridge_job.uuids)) ))
                    query = (bridge_job.bridge.insert().from_select(
                        [bridge_job.source_column, bridge_job.destination_column], select_query))
                        
                    c.execute(query)
                # handle self referential relationships
                for field_name in self_fields:
                    related_uuid = datum[field_name]
                    query = job.destination.update()
                        .values(job.destination.c[field_name] = job.destination.c.id)
                    # select_query = (select([job.destination.c.id])
                    #     .where(job.destination.c.uuid == related_uuid))
                    # query = job.destination.update()
                    #     .where(job.destination.c.uuid == datum['uuid'])


# TODO: sort what we save to respect the foreign key relationships (dependency graph?)
# TODO: figure out how to deal with M:M relationships on the same table (categories)
# ...???