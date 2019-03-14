import json
from collections import namedtuple
from marshmallow import Schema, fields, EXCLUDE, post_load, pre_load
from sqlalchemy import Table
from sqlalchemy.sql import select

from . import database
from .transformer import transformation
from .custom_fields import Related, RelatedMany


@transformation(source='raw_questions', destination=database.questions)
class QuestionSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        additional = ('stem', 'answer', 'distractor1', 'distractor2')
    id = fields.UUID(attribute='uuid')
    quiz_id = Related(database.quizzes)
    subjects = RelatedMany(
        related=database.subjects,
        bridge=database.question_subjects,
        source_column=database.question_subjects.c.question_id,
        destination_column=database.question_subjects.c.subject_id)

    @pre_load
    def deserialize_subjects(self, data):
        data['subjects'] = json.loads(data['subjects'])
        return data

    @post_load
    def set_data(self, data):
        data['uuid'] = str(data['uuid'])
        return data


@transformation(source='raw_quizzes', destination=database.quizzes)
class QuizSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        additional = ('name',)

    id = fields.UUID(attribute="uuid")

    @post_load
    def set_data(self, data):
        data['uuid'] = str(data['uuid'])
        data['slug'] = data['name'].lower().replace(' ', '-')
        return data


@transformation(source='raw_subjects', destination=database.subjects)
class SubjectSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        additional = 'name',

    id = fields.UUID(attribute="uuid")

    @post_load
    def set_data(self, data):
        data['uuid'] = str(data['uuid'])
        return data