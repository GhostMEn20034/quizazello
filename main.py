""" -*- coding: utf-8 -*-
Name: ~ Quizazello ~
About: This is a simple script for creating great tests and quizzes.
Author: Igor Markin
Blog: https://de0.ru
Email: 9588604@gmail.com
Version 0.5

"""

import sys
from collections import Counter
from difflib import SequenceMatcher as SMatcher
from random import choice

QUIZ_DB = 'quiz_db.dat'
SAVE_DB = 'save_questions.dat'
ACCURACY = 0.8
ROUNDS = 4
WIN_COST = 10
HINT_COST = 5


class Questions:

    def __init__(self):
        self.quiz_db = list()
        self.cost = 0
        self.points = 0
        self.record = 0

        self.commands = {
            '/exit': 'Questions are not saved.',
            '/exit -s': 'Questions are saved.'
        }

    @staticmethod
    def check_save():
        try:
            with open(SAVE_DB, 'r', encoding='utf-8'):
                pass
            return True
        except FileNotFoundError:
            return False

    def load_db(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as db:
                for line in db:
                    line = line.replace('\n', '').split('|')
                    self.quiz_db.append(tuple(line))
            self.points = int(self.quiz_db[0][0])
            self.record = int(self.quiz_db[0][1])
            del self.quiz_db[0]
        except FileNotFoundError:
            print('Error: file not found')

    def save_db(self):
        try:
            with open(SAVE_DB, 'w', encoding='utf-8') as db:
                db.write(f'{self.points}|{self.record}')
                for line in self.quiz_db:
                    db.write('\n' + '|'.join(line))
            return True
        except IOError:
            print('Error: failed to create file')

    def get_question(self, line):
        return self.quiz_db[line]

    def get_random_question(self):
        return choice(self.quiz_db)

    def delete_question(self, deleted_question):
        self.quiz_db.remove(deleted_question)

    @staticmethod
    def get_hint(answer, step):
        letters = Counter(list(answer)).most_common()
        if (' ', 1) in letters:
            letters.remove((' ', 1))
        for letter in range(step, len(letters)):
            answer = answer.replace(letters[letter][0], '*')
        return answer

    @staticmethod
    def get_similarity(answer, user_answer_):
        similarity = SMatcher(None, answer.lower(),
                              user_answer_.lower()).ratio()
        return similarity

    def run(self, command):
        if command in self.commands.keys():
            if command == '/exit':
                input(f'\n{self.commands[command]} Press Enter to exit...')
                sys.exit()
            elif command == '/exit -s':
                quiz.save_db()
                input(f'\n{self.commands[command]} Press Enter to exit...')
                sys.exit()


class Screens:

    def __init__(self):
        print('=' * 52)
        print('============ WELCOME TO ~ QUIZAZELLO ~ =============')
        print('=' * 52)
        print('RULES:\n'
              '▶ The computer asks and you answer\n'
              f'▶ You pay {HINT_COST} ✪ for incorrect answers\n'
              f'▶ You earn from {WIN_COST} ✪ for correct answers')
        print('-' * 52)

    @staticmethod
    def status(points, record, question_, cost_):
        print(f'\nYou have {points} ✪ | '
              f'Your record is {record} ✪ | '
              f'You can earn {cost_} ✪')
        print(f'Question: {question_}.')


if __name__ == '__main__':

    quiz = Questions()
    screen = Screens()

    if quiz.check_save():
        select = ''
        while select not in ('y', 'n'):
            select = input('\nDo you want to load a save file? (y/n): ')
            if select == 'y':
                quiz.load_db(SAVE_DB)
            elif select == 'n':
                quiz.load_db(QUIZ_DB)
    else:
        quiz.load_db(QUIZ_DB)

    play_game = True

    while play_game:

        play_round = True

        while play_round:

            question = quiz.get_random_question()
            quiz.cost = WIN_COST + len(question[1])

            screen.status(quiz.points, quiz.record, question[0], quiz.cost)

            for i in range(ROUNDS):
                user_answer = input('Your answer: ')

                quiz.run(user_answer)

                if quiz.get_similarity(question[1], user_answer) >= ACCURACY:
                    quiz.points += quiz.cost
                    break

                quiz.points -= HINT_COST
                print(f'\nNo, not "{user_answer}". You lost {HINT_COST} ✪.')

                if i < ROUNDS - 1:
                    print(f'Hint: {quiz.get_hint(question[1], i)}.')
            else:
                input('\nSorry, you have not guessed the correct answer. '
                      'Press Enter...')
                break

            quiz.delete_question(question)

            input(f'\nThat is right - "{question[1]}". '
                  f'You have earned {quiz.cost} ✪. Press Enter...')

            if quiz.points > quiz.record:
                quiz.record = quiz.points

            quiz.save_db()
