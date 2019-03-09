from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

engine = create_engine("sqlite:///test.db", echo=True)
meta = MetaData(bind=engine)

tests = Table('tests', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
)

questions = Table('questions', meta,
    Column('id', Integer, primary_key=True),
    Column('stem', String),
    Column('answer', String),
    Column('distractor1', String),
    Column('distractor2', String),
)
