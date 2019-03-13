from marshmallow import Schema, fields, EXCLUDE, post_load
from sqlalchemy.sql import select

from . import database
from .transformer import transformation


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
 

class Related(fields.Field):
    def __init__(self, table):
        super().__init__(self, load_only=True)
        self.table = table

    def _deserialize(self, value, attr, data, **kwargs):
        query = select([self.table.c.id]).where(
            self.table.c.uuid == value)
        with database.engine.connect() as c:
            result = c.execute(query)
            return result.fetchone().id


@transformation(source='raw_questions', destination=database.questions)
class QuestionSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        additional = ('stem', 'answer', 'distractor1', 'distractor2')
    id = fields.UUID(attribute='uuid')
    quiz_id = Related(database.quizzes)
 
    @post_load
    def set_data(self, data):
        data['uuid'] = str(data['uuid'])
        return data