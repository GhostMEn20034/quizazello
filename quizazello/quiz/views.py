from django.shortcuts import render

from .services import start_new_game


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


def undex(request):
    if not request.session.session_key:
        start_new_game(request)

    if request.method == 'POST':
        player_answer = request.POST['answer']
        correct_answer = request.session['answer']
        check_player_answer(player_answer, correct_answer)

    return render(request, 'index.html')

