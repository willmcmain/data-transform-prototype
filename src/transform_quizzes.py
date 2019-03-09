from marshmallow import Schema, fields, EXCLUDE, post_load
from transformer import transformation


@transformation(source='raw_quizzes', destination='quizzes')
class QuizSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        additional = ('name',)

    id = fields.UUID(attribute="uuid")

    @post_load
    def set_slug(self, data):
        data['slug'] = data['name'].lower().replace(' ', '-')
        return data
