from django.shortcuts import render

from .services import Game


def index(request):
    if request.session.session_key is None:
        request.session['step'] = 0
        request.session['right'] = 0
        request.session['wrong'] = 0
        request.session['hint'] = ''
        request.session['question'] = ''
        request.session['answer'] = ''

    session_key = request.session.session_key
    result = 'Вопрос:'

    if request.method == 'POST':
        request.session['step'] += 1
        request.session['hint'] = Game.get_hint(request.session['answer'],
                                                request.session['step'])

        if Game.correct_answer(request.session['answer'],
                               request.POST['answer']):
            result = f'Правильно — {request.session["answer"]}!'
            request.session['step'] = 0
            request.session['hint'] = ''
            request.session['right'] += 1
        else:
            result = 'Неправильно! Вот подсказка:'

        if request.session['step'] >= 3:
            result = f'Вы не угадали: {request.session["answer"]}!'
            request.session['step'] = 0
            request.session['hint'] = ''
            request.session['wrong'] += 1

    if request.session['step'] == 0:
        question = Game.get_random_question()
        request.session['question'] = question.question
        request.session['answer'] = question.answer

    context = {
        'question': request.session['question'],
        'answer': request.session['answer'],
        'result': result,
        'hint': request.session['hint'],
        'step': request.session['step'],
        'right': request.session['right'],
        'wrong': request.session['wrong'],
    }

    request.session.modified = True

    return render(request, 'index.html', context)
