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
from random import choice, randint

QUIZ_DB = 'quiz_db.dat'
SAVE_DB = 'save_questions.dat'
ACCURACY = 0.8
ROUNDS = 4
WIN_COST = 10
HINT_COST = 3
GAME_CHANCE = 0  # 0-100


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
    def run(question, command):
        commands = {
            '/exit': 'Questions not saved.',
            '/exit -s': 'Questions saved.'
        }

        if command in commands.keys():
            if command == '/exit':
                input(f'\n{commands[command]} Press Enter to exit...')
                sys.exit()
            elif command == '/exit -s':
                question.save_db()
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
    def check_answer(question):
        for i in range(ROUNDS):
            user_answer = input('Your answer: ')

            Service.run(command=user_answer, question=question)

            if Service.similarity(question.answer, user_answer) >= ACCURACY:
                question.points += question.cost
                return True

            question.points -= HINT_COST
            print(f'\nNo, not "{user_answer}". You lost {HINT_COST} ✪.')

            if i < ROUNDS - 1:
                print(f'Hint: {Service.hint(quiz.answer, i)}.')
        else:
            input('\nSorry, you not guessed the correct answer. '
                  'Press Enter...')
            return False

    @staticmethod
    def correct_answer(question):
        question.delete_question((question.question, question.answer))
        input(f'\nThat is right - "{question.answer}". '
              f'You earned {question.cost} ✪. Press Enter...')

        if question.points > question.record:
            question.record = question.points

        question.save_db()

    @staticmethod
    def start_round(question):
        question.question, question.answer = question.get_random_question()
        question.cost = WIN_COST + len(question.answer)

    @staticmethod
    def random_game(question):
        if 1 < randint(1, 100) <= GAME_CHANCE:
            Game.guess_number(question)


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


class Game:

    @staticmethod
    def guess_number(question):
        random_number = randint(1, 10)
        user_number = ''
        while not user_number.isdigit():
            user_number = input(f'\nGuess a number from 1 to 10: ')
        if int(user_number) == random_number:
            print(f'Good! You wined {question.cost} ✪')
            question.points += question.cost
            input('Press Enter...')
        else:
            input('Sorry! You lost. Press Enter...')
        return True


if __name__ == '__main__':

    quiz = Question()
    Screen.start_screen()
    quiz.load_db(filename=Service.select_db())

    play_game = True
    while play_game:

        play_round = True
        while play_round:

            Service.start_round(question=quiz)
            Service.random_game(quiz)
            Screen.status(points=quiz.points, record=quiz.record,
                          question_=quiz.question, cost_=quiz.cost)

            if not Service.check_answer(question=quiz):
                break
            else:
                Service.correct_answer(question=quiz)
