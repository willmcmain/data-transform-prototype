import pytest
from .transformer import topological_sort_jobs


test_graph = {
    'questions': {
        'dependencies':['quizzes', 'subjects'],
        'job': 'questions',
    },
    'quizzes': {
        'dependencies': None,
        'job': 'quizzes',
    },
    'subjects': {
        'dependencies': ['authors'],
        'job': 'subjects',
    },
    'authors':{
        'dependencies': ['quizzes'],
        'job': 'authors',
    },
}

cycle_graph = {
    'questions': {
        'dependencies':['quizzes', 'subjects'],
        'job': 'questions',
    },
    'quizzes': {
        'dependencies': None,
        'job': 'quizzes',
    },
    'subjects': {
        'dependencies': ['authors', 'questions'],
        'job': 'subjects',
    },
    'authors':{
        'dependencies': ['quizzes'],
        'job': 'authors',
    },
}


def test_topological_sort_jobs():
    expected_list = ['quizzes', 'authors', 'subjects', 'questions']
    actual_list = topological_sort_jobs(test_graph)

    assert expected_list == actual_list


def test_topological_sort_jobs_cycle():
    with pytest.raises(ValueError) as e:
        topological_sort_jobs(cycle_graph)