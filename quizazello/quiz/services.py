from collections import Counter
from difflib import SequenceMatcher as SMatcher
from random import randint

from .models import Quiz


class Game:

    @staticmethod
    def new(request):
        Game.get_question(request)
        request.session['result'] = 'Вопрос:'
        request.session['step'] = 0
        request.session['right'] = 0
        request.session['wrong'] = 0
        return request

    @staticmethod
    def win(request):
        result = f'Правильно: {request.session["answer"]}! Играем дальше.'
        request.session['result'] = result
        request.session['step'] = 0
        request.session['right'] += 1
        Game.get_question(request)
        return request

    @staticmethod
    def lose(request):
        if request.session['step'] >= 3:
            result = f'Не угадали: {request.session["answer"]}. Играем дальше.'
            request.session['step'] = 0
            request.session['wrong'] += 1
            Game.get_question(request)
        else:
            result = 'Неправильно. Попробуйте ещё.'
            request.session['step'] += 1
            request.session['hint'] = Game.get_hint(request.session['answer'],
                                                    request.session['step'])

        request.session['result'] = result
        return request

    @staticmethod
    def get_question(request):
        pk = randint(1, Quiz.objects.count())
        question = Quiz.objects.all().get(pk=pk)
        request.session['question'] = question.question
        request.session['answer'] = question.answer
        request.session['hint'] = Game.get_hint(question.answer)
        return request

    @staticmethod
    def correct_answer(answer, user_answer):
        similarity = SMatcher(None, answer.lower(), user_answer.lower())
        return similarity.ratio() >= 0.8

    @staticmethod
    def get_hint(answer, step=0):
        letters = Counter(list(answer)).most_common()
        if (' ', 1) in letters:
            letters.remove((' ', 1))
        for letter in range(step, len(letters)):
            answer = answer.replace(letters[letter][0], '*')
        return answer
