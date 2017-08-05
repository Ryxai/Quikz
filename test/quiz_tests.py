import pytest
from src.quikz import Quiz


#Quiz API Tests

def test_quiz_and_properties_exists():
    #Instance
    quiz = Quiz()
    assert isinstance(quiz, Quiz)
    #Basic Methods
    assert quiz.length() == 0
    assert quiz.questions() == []
    assert quiz.answer_key() == []
    #Methods
    assert hasattr(quiz, "add_question")
    assert hasattr(quiz, "delete_question") assert hasattr(quiz, "get_question")
    assert hasattr(quiz, "get_prompt")
    assert hasattr(quiz, "get_answer")
    assert hasattr(quiz, "get_choices")
    assert hasattr(quiz, "clear")
    assert hasattr(quiz, "shuffle")
    assert hasattr(quiz, "copy")

def test_quiz_question_manipulation():
    quiz = Quiz()
    assert quiz.length() == 0
    assert quiz.add_question("This is a question", "A", ["A", "B", "C", "D"])
    assert quiz.add_question("This is a question too", "Q", ["A", "B", "C"])
    assert not quiz.add_question("This is a question")
    assert not quiz.add_question(1, "A,", ["A", "B"])
    assert not quiz.add_question("Test", 2, ["A", "B", "C"])
    assert not quiz.add_question("Test", 2, ["A", 2, "C"])
    assert quiz.length() == 2

def test_quiz_delete_questions():
    quiz = Quiz()
    assert quiz.add_question("This is a question", "A", ["A", "B", "C", "D"])
    assert quiz.add_question("This is a question too", "Q", ["A", "B", "C"])
    assert quiz.delete_question(0)
    assert quiz.delete_question(0)
    assert not quiz.delete_question(0)
    assert quiz.add_question("This is a question", "A", ["A", "B", "C", "D"])
    assert quiz.add_question("This is a question too", "Q", ["A", "B", "C"])
    assert not quiz.delete_question(2)
    assert not quiz.delete_question(-1)

def test_quiz_get_question_details():
    quiz = Quiz()
    assert quiz.add_question("This is a question", "A", ["A", "B", "C", "D"])
    assert quiz.add_question("This is a question too", "Q", ["A", "B", "C"])
    assert quiz.get_question(0) == ("This is a question", "A", ["A", "B", "C",
                                                                "D"])
    assert quiz.get_question(1) == ("This is a question too", "Q", ["A", "B",
                                                                    "C"])
    assert pytest.raises(ValueError, quiz.get_question(2))
    assert pytest.raises(ValueError, quiz.get_question(-1))


def test_quiz_get_prompt():
    quiz = Quiz()
    assert quiz.add_question("This is a question", "A", ["A", "B", "C", "D"])
    assert quiz.add_question("This is a question too", "Q", ["A", "B", "C"])
    assert quiz.get_prompt(0) == "This is a question"
    assert quiz.get_prompt(1) == "This is a question too"
    assert pytest.raises(ValueError,quiz.get_prompt(3))
    assert pytest.raises(ValueError, quiz.get_prompt(-1))

def test_quiz_get_answer():
    quiz = Quiz()
    assert quiz.add_question("This is a question", "A", ["A", "B", "C", "D"])
    assert quiz.add_question("This is a question too", "Q", ["A", "B", "C"])
    assert quiz.get_answer(0) == "A"
    assert quiz.get_answer(1) == "Q"
    assert pytest.raises(ValueError, quiz.get_answer(2))
    assert pytest.raises(ValueError, quiz.get_answer(-1))

def test_quiz_get_choices():
    quiz = Quiz()
    assert quiz.add_question("This is a question", "A", ["A", "B", "C", "D"])
    assert quiz.add_question("This is a question too", "Q", ["A", "B", "C"])
    assert quiz.get_choices(0) == ["A", "B", "C", "D"]
    assert quiz.get_choices(1) == ["A", "B", "C"]
    assert pytest.raises(ValueError, quiz.get_choices(2))
    assert pytest.raises(ValueError, quiz.get_choices(-1))

def test_quiz_clear():
    quiz = Quiz()
    assert quiz.add_question("This is a question", "A", ["A", "B", "C", "D"])
    assert quiz.add_question("This is a question too", "Q", ["A", "B", "C"])
    assert len(quiz) == 2
    quiz.clear()
    assert len(quiz) == 0

def test_quiz_shuffle():
    quiz = Quiz()
    assert quiz.add_question("This is a question", "A", ["A", "B", "C", "D"])
    assert quiz.add_question("This is a question too", "Q", ["A", "B", "C"])
    hash_before_shuffle = hash(quiz)
    quiz.shuffle()
    assert quiz.length() == 2
    assert hash(quiz) == hash_before_shuffle

def test_quiz_copy():
    quiz = Quiz()
    assert quiz.add_question("This is a question", "A", ["A", "B", "C", "D"])
    assert quiz.add_question("This is a question too", "Q", ["A", "B", "C"])
    second_quiz = quiz.copy()
    assert hash(quiz) == hash(second_quiz)
    assert second_quiz.length == 2
