""" -*- coding: utf-8 -*-
Name: ~ Quizazello ~
About: This is a simple script for creating great tests and quizzes.
Author: Igor Markin
Blog: https://de0.ru
Email: 9588604@gmail.com
Version 0.6
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
HINT_COST = 3


class Question:

    def __init__(self):
        self.quiz_db = list()
        self.question = ''
        self.answer = ''
        self.cost = 0
        self.points = 0
        self.record = 0

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


class Service:

    @staticmethod
    def run(questions, command):
        commands = {
            '/exit': 'Questions not saved.',
            '/exit -s': 'Questions saved.'
        }

        if command in commands.keys():
            if command == '/exit':
                input(f'\n{commands[command]} Press Enter to exit...')
                sys.exit()
            elif command == '/exit -s':
                questions.save_db()
                input(f'\n{commands[command]} Press Enter to exit...')
                sys.exit()

    @staticmethod
    def select_db():
        try:
            with open(SAVE_DB, 'r', encoding='utf-8'):
                pass
            select = ''
            while select not in ('y', 'n'):
                select = input('\nDo you want to load a save file? (y/n): ')
                if select == 'y':
                    return SAVE_DB
                elif select == 'n':
                    return QUIZ_DB
        except FileNotFoundError:
            return QUIZ_DB

    @staticmethod
    def hint(answer, step):
        letters = Counter(list(answer)).most_common()
        if (' ', 1) in letters:
            letters.remove((' ', 1))
        for letter in range(step, len(letters)):
            answer = answer.replace(letters[letter][0], '*')
        return answer

    @staticmethod
    def similarity(answer, user_answer_):
        similarity = SMatcher(None, answer.lower(),
                              user_answer_.lower()).ratio()
        return similarity

    @staticmethod
    def check_answer(questions):
        for i in range(ROUNDS):
            user_answer = input('Your answer: ')

            Service.run(command=user_answer, questions=questions)

            if Service.similarity(questions.answer, user_answer) >= ACCURACY:
                questions.points += questions.cost
                return True

            questions.points -= HINT_COST
            print(f'\nNo, not "{user_answer}". You lost {HINT_COST} ✪.')

            if i < ROUNDS - 1:
                print(f'Hint: {Service.hint(quiz.answer, i)}.')
        else:
            input('\nSorry, you not guessed the correct answer. '
                  'Press Enter...')
            return False

    @staticmethod
    def correct_answer(questions):
        questions.delete_question((questions.question, questions.answer))
        input(f'\nThat is right - "{questions.answer}". '
              f'You earned {questions.cost} ✪. Press Enter...')

        if questions.points > questions.record:
            questions.record = questions.points

        questions.save_db()

    @staticmethod
    def start_round(questions):
        questions.question, questions.answer = questions.get_random_question()
        questions.cost = WIN_COST + len(questions.answer)


class Screen:

    @staticmethod
    def start_screen():
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

    quiz = Question()
    Screen.start_screen()
    quiz.load_db(filename=Service.select_db())

    play_game = True
    while play_game:

        play_round = True
        while play_round:

            Service.start_round(questions=quiz)
            Screen.status(points=quiz.points, record=quiz.record,
                          question_=quiz.question, cost_=quiz.cost)
            if not Service.check_answer(questions=quiz):
                break
            else:
                Service.correct_answer(questions=quiz)
