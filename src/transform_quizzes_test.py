from sqlalchemy.sql import select
from uuid import UUID

from database import init_database, quizzes, engine
from transformer import run
from transform_quizzes import QuizSchema


def test_quiz_schema_load():
    expected = {
        'uuid': 'd6b31381-5669-4eb6-a2cf-3bf5dff63980',
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


def test_transform_raw_data():
    init_database()
    run()

    query = (select([quizzes])
        .where(quizzes.c.uuid == '20a68f42-412d-4348-8a3d-0ae41d00800a'))

    with engine.connect() as c:
        result = c.execute(query)
        quiz = result.fetchone()

    assert quiz.name == 'Cat Herding'
    assert quiz.slug == 'cat-herding'
