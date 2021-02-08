from collections import Counter
from difflib import SequenceMatcher as SMatcher
from random import randint

from .models import Quiz


def get_question() -> tuple:
    pk = randint(1, Quiz.objects.count())
    question = Quiz.objects.get(pk=pk)
    return question


def get_hint(answer: str, step: int = 0) -> str:
    letters = Counter(list(answer)).most_common()
    letters_length = len(letters)
    hint = answer
    space = (' ', 1)
    if space in letters:
        letters.remove(space)
    for letter in range(step, letters_length):
        letter = letters[letter][0]
        hint = hint.replace(letter, '*')
    return hint


def start_new_game(request):
    question, answer = get_question()
    hint = get_hint(answer)
    request.session |= {
        'result': 'Вопрос:',
        'step': 0,
        'right': 0,
        'wrong': 0,
        'question': question,
        'answer': answer,
        'hint': hint,
    }
    return request


def win(request):
    result = f'Правильно: {request.session["answer"]}! Играем дальше.'
    request.session['result'] = result
    request.session['step'] = 0
    request.session['right'] += 1
    get_question()
    return request


def lose(request):
    if request.session['step'] >= 3:
        result = f'Не угадали: {request.session["answer"]}. Играем дальше.'
        request.session['step'] = 0
        request.session['wrong'] += 1
        get_question()
    else:
        result = 'Неправильно. Попробуйте ещё.'
        request.session['step'] += 1
        request.session['hint'] = get_hint(request.session['answer'],
                                           request.session['step'])

    request.session['result'] = result
    return request


def check_player_answer(answer, user_answer):
    similarity = SMatcher(None, answer.lower(), user_answer.lower())
    return similarity.ratio() >= 0.8
