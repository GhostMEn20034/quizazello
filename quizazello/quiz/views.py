from django.shortcuts import render

from .services import Game


def index(request):
    if not request.session.session_key:
        Game.new(request)

    if request.method == 'POST':
        answer = request.session['answer']
        user_answer = request.POST['answer'] or None

        if Game.correct_answer(answer, user_answer):
            Game.win(request)
        else:
            Game.lose(request)

    request.session.modified = True
    return render(request, 'index.html')
