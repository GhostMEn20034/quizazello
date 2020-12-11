from django.shortcuts import render

from .services import Game


def index(request):
    if not request.session.session_key:
        question = Game.get_random_question()
        request.session['question'] = question.question
        request.session['answer'] = question.answer
        request.session['step'] = 0
        request.session['hint'] = Game.get_hint(request.session['answer'],
                                                request.session['step'])
        request.session['result'] = 'Вопрос:'
        request.session['right'] = 0
        request.session['wrong'] = 0

    if request.method == 'POST':
        if Game.correct_answer(request.session['answer'],
                               request.POST['answer']):
            request.session['result'] = ('Правильно: '
                                         f'{request.session["answer"]}! '
                                         'Поехали дальше.')
            request.session['step'] = 0
            request.session['right'] += 1
            question = Game.get_random_question()
            request.session['question'] = question.question
            request.session['answer'] = question.answer
            request.session['hint'] = Game.get_hint(request.session['answer'],
                                                    request.session['step'])
        else:
            request.session['result'] = 'Неправильно. Попробуйте ещё.'
            request.session['step'] += 1
            request.session['hint'] = Game.get_hint(request.session['answer'],
                                                    request.session['step'])

        if request.session['step'] >= 3:
            request.session['result'] = ('Не угадали: '
                                         f'{request.session["answer"]}. '
                                         'Поехали дальше.')
            question = Game.get_random_question()
            request.session['question'] = question.question
            request.session['answer'] = question.answer
            request.session['step'] = 0
            request.session['hint'] = Game.get_hint(request.session['answer'],
                                                    request.session['step'])
            request.session['wrong'] += 1

    request.session.modified = True

    context = {
        'question': request.session['question'],
        'answer': request.session['answer'],
        'hint': request.session['hint'],
        'result': request.session['result'],
        'step': request.session['step'],
        'right': request.session['right'],
        'wrong': request.session['wrong'],
    }

    return render(request, 'index.html', context)
