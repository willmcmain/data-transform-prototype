import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey

engine = create_engine("sqlite:///test.db")
meta = MetaData(bind=engine)

quizzes = Table('quizzes', meta,
    Column('id', Integer, primary_key=True),
    Column('uuid', String),
    Column('slug', String),
    Column('name', String),
)

questions = Table('questions', meta,
    Column('id', Integer, primary_key=True),
    Column('quiz_id', None, ForeignKey('quizzes.id')),
    Column('uuid', String),
    Column('stem', String),
    Column('answer', String),
    Column('distractor1', String),
    Column('distractor2', String),
)

subjects = Table('subjects', meta,
    Column('id', Integer, primary_key=True),
    Column('uuid', String),
    Column('name', String),
    Column('parent_id', Integer)
)

question_subjects = Table('question_subjects', meta,
    Column('question_id', None, ForeignKey('questions.id')),
    Column('subject_id', None, ForeignKey('subjects.id'))
)


def init_database():
    try:
        os.remove('test.db')
    except FileNotFoundError:
        pass
    os.system('cat test.sql | sqlite3 test.db')
    meta.create_all()
