from transform_quizzes import QuizSchema
from uuid import UUID


def test_quiz_schema_load():
    expected = {
        'uuid': UUID('d6b31381-5669-4eb6-a2cf-3bf5dff63980'),
        'name': 'Advanced Rocket Science',
        'slug': 'advanced-rocket-science'
    }

    raw = {
        'id': 'd6b31381-5669-4eb6-a2cf-3bf5dff63980',
        'name': "Advanced Rocket Science"
    }
    schema = QuizSchema()
    actual = schema.load(raw)
    assert actual == expected
