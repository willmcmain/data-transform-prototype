import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

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
    Column('uuid', String),
    Column('stem', String),
    Column('answer', String),
    Column('distractor1', String),
    Column('distractor2', String),
)


def init_database():
    os.remove('test.db')
    os.system('cat test.sql | sqlite3 test.db')

    meta.create_all()
