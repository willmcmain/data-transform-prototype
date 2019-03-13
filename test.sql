DROP TABLE IF EXISTS raw_quizzes;
CREATE TABLE raw_quizzes (
    id VARCHAR PRIMARY KEY,
    name VARCHAR
);

DROP TABLE IF EXISTS raw_subjects;
CREATE TABLE raw_subjects (
    id VARCHAR PRIMARY KEY,
    name VARCHAR
);

DROP TABLE IF EXISTS raw_questions;
CREATE TABLE raw_questions (
    id VARCHAR PRIMARY KEY,
    quiz_id VARCHAR,
    stem VARCHAR,
    answer VARCHAR,
    distractor1 VARCHAR,
    distractor2 VARCHAR,
    subjects VARCHAR
);

INSERT INTO raw_quizzes VALUES
    ("20a68f42-412d-4348-8a3d-0ae41d00800a", "Cat Herding"),
    ("447ab859-dad6-41f7-94a7-6e721f3041e2", "Python");

INSERT INTO raw_subjects VALUES
    ("0b32a063-a728-4635-8938-4dfc6f0a059a", "Basic Cat Herding"),
    ("fa2c0919-af36-48df-9576-a48302c8de6f", "Advanced Cat Herding"),
    ("debf0cba-9919-4a7a-b01f-3a0233fe65f0", "Variables"),
    ("82f02bca-72f2-40fd-8772-634d9afd7667", "For Loops");

INSERT INTO raw_questions VALUES
    (
        "30def45b-47f0-4806-aa7f-e200c647d4ec",
        "20a68f42-412d-4348-8a3d-0ae41d00800a",
        "How do herd cats?",
        "They're cats",
        "Yes",
        "No",
        '["0b32a063-a728-4635-8938-4dfc6f0a059a", "fa2c0919-af36-48df-9576-a48302c8de6f"]'
    ),
    (
        "2f5ab47b-529d-48ac-b142-5b2e93a45b83",
        "447ab859-dad6-41f7-94a7-6e721f3041e2",
        "How do you use a for loop?",
        "for:",
        "while:",
        "but:",
        '["82f02bca-72f2-40fd-8772-634d9afd7667"]'
    );
