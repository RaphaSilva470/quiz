import pytest
from model import Question, Choice


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

def test_add_multiple_choices_generates_incremental_ids():
    question = Question(title="q1")
    c1 = question.add_choice("a")
    c2 = question.add_choice("b")
    assert c2.id == c1.id + 1


def test_remove_choice_by_id_removes_correct_choice():
    question = Question(title="q1")
    c1 = question.add_choice("a")
    question.remove_choice_by_id(c1.id)
    assert len(question.choices) == 0


def test_remove_choice_by_id_with_invalid_id_raises():
    question = Question(title="q1")
    question.add_choice("a")
    with pytest.raises(Exception):
        question.remove_choice_by_id(999)


def test_remove_all_choices_clears_choices():
    question = Question(title="q1")
    question.add_choice("a")
    question.add_choice("b")
    question.remove_all_choices()
    assert question.choices == []


def test_set_correct_choices_marks_choices_as_correct():
    question = Question(title="q1")
    c1 = question.add_choice("a")
    c2 = question.add_choice("b")
    question.set_correct_choices([c2.id])
    assert not c1.is_correct
    assert c2.is_correct


def test_set_correct_choices_with_invalid_id_raises():
    question = Question(title="q1")
    question.add_choice("a")
    with pytest.raises(Exception):
        question.set_correct_choices([999])


def test_correct_selected_choices_returns_only_correct():
    question = Question(title="q1", max_selections=2)  # permite duas seleções
    c1 = question.add_choice("a")
    c2 = question.add_choice("b", is_correct=True)
    result = question.correct_selected_choices([c1.id, c2.id])
    assert result == [c2.id]


def test_correct_selected_choices_respects_max_selections():
    question = Question(title="q1", max_selections=1)
    c1 = question.add_choice("a", True)
    c2 = question.add_choice("b", True)
    with pytest.raises(Exception):
        question.correct_selected_choices([c1.id, c2.id])


def test_choice_text_cannot_be_empty():
    with pytest.raises(Exception):
        Choice(id=1, text="")


def test_choice_text_cannot_exceed_100_chars():
    with pytest.raises(Exception):
        Choice(id=1, text="a" * 101)