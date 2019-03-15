from sqlalchemy.sql import select
from uuid import UUID

from .database import init_database, quizzes, engine, subjects, questions, question_subjects
from .transformer import run
from .transform_quizzes import QuizSchema


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

    query = (select([subjects])
        .where(subjects.c.uuid == '0b32a063-a728-4635-8938-4dfc6f0a059a'))

    with engine.connect() as c:
        result = c.execute(query)
        subject = result.fetchone()

    assert subject.name == 'Basic Cat Herding'

    query = (select([questions])
        .where(questions.c.uuid == '30def45b-47f0-4806-aa7f-e200c647d4ec'))

    with engine.connect() as c:
        result = c.execute(query)
        question = result.fetchone()

    assert question.stem == 'How do herd cats?'
    assert question.quiz_id == quiz.id

    query = (select([question_subjects])
        .where((question_subjects.c.question_id == question.id)
        & (question_subjects.c.subject_id == subject.id)))
    with engine.connect() as c:
        result = c.execute(query)
        question_subject = result.fetchone()

    assert question_subject is not None

    query = (select([subjects])
        .where(subjects.c.uuid == 'fa2c0919-af36-48df-9576-a48302c8de6f'))

    with engine.connect() as c:
        result = c.execute(query)
        subject_advanced = result.fetchone()

    assert subject_advanced.parent_id == subject.id