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

import settings


class QuizDB:

    def __init__(self):
        self.quiz_db = list()
        self.question = ''
        self.answer = ''
        self.cost = 0
        self.points = 0
        self.record = 0

    @staticmethod
    def select_db():
        try:
            with open(settings.SAVE_DB, 'r', encoding='utf-8'):
                pass
            select = ''
            while select not in ('y', 'n'):
                select = input('\nDo you want to load the save file? (y/n): ')
                if select == 'y':
                    return settings.SAVE_DB
                elif select == 'n':
                    return settings.QUIZ_DB
        except FileNotFoundError:
            return settings.QUIZ_DB

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
            with open(settings.SAVE_DB, 'w', encoding='utf-8') as db:
                db.write(f'{self.points}|{self.record}')
                for line in self.quiz_db:
                    db.write('\n' + '|'.join(line))
            return True
        except IOError:
            print('Error: failed to create file')

    def get_random_question(self):
        return choice(self.quiz_db)

    def delete_question(self):
        self.quiz_db.remove((self.question, self.answer))

    def get_hint(self, step):
        hint = self.answer
        letters = Counter(list(self.answer)).most_common()
        if (' ', 1) in letters:
            letters.remove((' ', 1))
        for letter in range(step, len(letters)):
            hint = hint.replace(letters[letter][0], '*')
        return hint

    def check_similarity(self, user_answer):
        similarity = SMatcher(None, self.answer.lower(),
                              user_answer.lower()).ratio()
        return similarity

    def correct_answer(self):
        for i in range(settings.ROUNDS):
            user_answer = input('Your answer: ')
            self.check_command(user_answer)

            if self.check_similarity(user_answer) >= settings.ACCURACY:
                self.points += self.cost
                quiz.delete_question()
                return True

            self.points -= settings.HINT_COST
            print(f'\nNo, not "{user_answer}". '
                  f'You lost {settings.HINT_COST} ✪.')

            if i < settings.ROUNDS - 1:
                print(f'Hint: {self.get_hint(i)}')
        else:
            input('\nYou not guessed the correct answer. Press Enter...')
            return False

    def start_round(self):
        self.question, self.answer = self.get_random_question()
        self.cost = settings.WIN_COST + len(self.answer)

    def status(self):
        print(f'\nYou have {self.points} ✪ | '
              f'Your record is {self.record} ✪ | '
              f'You can earn {self.cost} ✪')
        print(f'Question: {self.question}.')

    def win_round(self):
        input(f'\nThat is right - "{self.answer}". '
              f'You earned {self.cost} ✪. Press Enter...')

    def update_record(self):
        if self.points > self.record:
            self.record = self.points

    def check_command(self, command):
        commands = {
            '/exit': 'Questions not saved.',
            '/exit -s': 'Questions saved.'
        }

        if command in commands.keys():
            if command == '/exit':
                input(f'\n{commands[command]} Press Enter to exit...')
                sys.exit()
            elif command == '/exit -s':
                self.save_db()
                input(f'\n{commands[command]} Press Enter to exit...')
                sys.exit()


if __name__ == '__main__':

    print('=' * 52)
    print('============ WELCOME TO ~ QUIZAZELLO ~ =============')
    print('=' * 52)

    quiz = QuizDB()
    quiz.load_db(filename=quiz.select_db())

    play_game = True
    while play_game:

        play_round = True
        while play_round:

            quiz.start_round()
            quiz.status()

            if not quiz.correct_answer():
                break

            quiz.update_record()
            quiz.save_db()
