from collections import Counter
from difflib import SequenceMatcher as SMatcher
from random import randint

from .models import Quiz


class Game:

    question = ''
    answer = ''
    question_number = 0
    questions_count = Quiz.objects.count()

    @staticmethod
    def get_random_question():
        question_number = randint(1, Game.questions_count)
        full_question = Quiz.objects.all().get(pk=question_number)
        return full_question

    @staticmethod
    def correct_answer(answer, user_answer):
        similarity = SMatcher(None, answer.lower(),
                              user_answer.lower())
        if similarity.ratio() >= 0.8:
            return True
        else:
            return False

    @staticmethod
    def get_hint(answer, step):
        letters = Counter(list(answer)).most_common()
        if (' ', 1) in letters:
            letters.remove((' ', 1))
        for letter in range(step, len(letters)):
            answer = answer.replace(letters[letter][0], '*')
        return answer
