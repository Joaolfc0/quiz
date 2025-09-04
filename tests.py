import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct


def test_add_multiple_choices_assigns_incremental_ids():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    c3 = question.add_choice('c')
    assert [c1.id, c2.id, c3.id] == [1, 2, 3]


def test_remove_choice_by_id_removes_choice():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    question.add_choice('b')
    question.remove_choice_by_id(c1.id)
    remaining_ids = [c.id for c in question.choices]
    assert remaining_ids == [2]


def test_remove_choice_by_id_invalid_raises():
    question = Question(title='q1')
    question.add_choice('a')
    with pytest.raises(Exception):
        question.remove_choice_by_id(999)


def test_remove_all_choices_empties_list():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_all_choices()
    assert question.choices == []


def test_set_correct_choices_marks_correct_flags():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    question.set_correct_choices([c2.id])
    assert not question.choices[0].is_correct
    assert question.choices[1].is_correct


def test_set_correct_choices_with_invalid_id_raises():
    question = Question(title='q1')
    question.add_choice('a')
    with pytest.raises(Exception):
        question.set_correct_choices([999])


def test_correct_selected_choices_exceeds_max_raises():
    question = Question(title='q1', max_selections=1)
    c1 = question.add_choice('a', is_correct=True)
    c2 = question.add_choice('b', is_correct=False)
    with pytest.raises(Exception):
        question.correct_selected_choices([c1.id, c2.id])


def test_correct_selected_choices_returns_only_correct():
    question = Question(title='q1', max_selections=3)
    c1 = question.add_choice('a', is_correct=True)
    c2 = question.add_choice('b', is_correct=False)
    c3 = question.add_choice('c', is_correct=True)
    returned = question.correct_selected_choices([c1.id, c2.id, c3.id])
    assert set(returned) == {c1.id, c3.id}


def test_title_boundary_lengths_valid():
    assert Question(title='a', points=1).title == 'a'
    title_200 = 'x' * 200
    assert Question(title=title_200, points=10).title == title_200


def test_choice_text_boundaries():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('')
    with pytest.raises(Exception):
        question.add_choice('x' * 101)
    ok = question.add_choice('x' * 100)
    assert ok.text == 'x' * 100

@pytest.fixture
def question_with_choices():
    q = Question(title='question with choices', max_selections=2)
    a = q.add_choice('A', is_correct=True)
    b = q.add_choice('B', is_correct=False)
    c = q.add_choice('C', is_correct=True)
    return q, a, b, c


def test_fixture_returns_expected_choice_count(question_with_choices):
    q, a, b, c = question_with_choices
    assert [ch.id for ch in q.choices] == [a.id, b.id, c.id]
    assert len(q.choices) == 3


def test_correct_selected_choices_with_fixture(question_with_choices):
    q, a, b, c = question_with_choices
    result = q.correct_selected_choices([a.id, b.id])
    assert result == [a.id]