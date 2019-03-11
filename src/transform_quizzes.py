from marshmallow import Schema, fields, EXCLUDE, post_load

import database
from transformer import transformation


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
