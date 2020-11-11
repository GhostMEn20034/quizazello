# -*- coding: utf-8 -*-
# Name: ~ Quizazello ~
# About: This is a simple script for creating great tests and quizzes.
# Author: Igor Markin
# Blog: https://de0.ru
# Email: 9588604@gmail.com
# Version 0.2

import sys
from collections import Counter
from difflib import SequenceMatcher
from random import choice

settings = {
    'QUIZ_DB': 'quiz_db.dat',
    'SAVE_DB': 'save_questions.dat',
    'ACCURACY': 0.8,
    'COUNT_HINTS': 4,
    'WIN_PRICE': 5
}


class Questions:

    def __init__(self):
        self.quiz_db = list()

    @staticmethod
    def check_save():
        try:
            with open(settings['SAVE_DB'], 'r', encoding='utf-8') as db:
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
        except FileNotFoundError:
            print('Error: file not found')

    def save_db(self):
        try:
            with open(settings['SAVE_DB'], 'w', encoding='utf-8') as db:
                db.write('~ Quizazello ~')
                for line in self.quiz_db:
                    db.write('\n' + '|'.join(line))
            return True
        except IOError:
            print('Error: failed to create file')

    def get_question(self, line):
        return self.quiz_db[line]

    def get_random_question(self):
        return choice(self.quiz_db)

    @staticmethod
    def get_hint(answer, step):
        letters = Counter(list(answer)).most_common()
        if (' ', 1) in letters:
            letters.remove((' ', 1))
        for i in range(step, len(letters)):
            answer = answer.replace(letters[i][0], '*')
        return answer


class QuizDB:

    @staticmethod
    def load_db(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as db:
                quiz_db = list()
                for line in db:
                    line = line.replace('\n', '').split('|')
                    quiz_db.append(line)
            return quiz_db
        except FileNotFoundError:
            print('Error: file not found')

    @staticmethod


    def select_db(db_save_true):
        if db_save_true:
            number = input('Загрузить сохранённую игру?\n'
                           'Enter. Да, загрузить | 1. Начать новую игру | 0. Выход\n'
                           'Ваш ответ: ')
            if number == '':
                return DB_SAVE_FILE
            elif number == '1':
                return DB_FILE
            else:
                press_enter('')
        else:
            return DB_FILE


def check_db_save():
    try:
        open(DB_SAVE_FILE, 'r', encoding='utf-8')
    except FileNotFoundError:
        return False
    else:
        return True


def press_enter(text):
    input(f'\n{text} Нажмите Enter, чтобы выйти из игры...')
    sys.exit()


def check_commands(text):
    if text == '/exit':
        save_db(questions)
        press_enter('Игра сохранена.')
    elif text == '/exit -s':
        press_enter('Игра не сохранена.')


def check_similarity(answer, text):
    ratio_similarity = SequenceMatcher(None, answer.lower(),
                                       text.lower()).ratio()
    return ratio_similarity


def check_answer(answer):
    similarity = 0
    i = 1
    while similarity < ACCURACY:
        text = input('Ваш ответ: ')

        check_commands(text)

        similarity = check_similarity(answer, text)
        if similarity > ACCURACY:
            return True

        if i >= COUNT_HINTS + 1:
            return False

        print(f'Нет, не {text}. Подсказка: {hint(answer, i - 1)}.')
        i += 1


def check_status():
    if not questions:
        press_enter('Все вопросы закончились.')
    elif points <= 0:
        press_enter('У вас 0 баллов.')


def status_screen():
    print(f'\n--- У вас {points}✪ --- '
          f'Рекорд {record}✪ ---')
    print(f'Вопрос: {question[0]}.')
    print(f'Стоимость вопроса - {cost}✪.')


def start_screen():
    print('-' * 60)
    print('               ДОБРО ПОЖАЛОВАТЬ В QUIZAZELLO\n'
          '                   викторина версии 0.2')
    print('-' * 60)
    print('Правила игры:\n'
          '- компьютер спрашивает, вы отвечаете\n'
          '- после двух неправильных ответов он даст вам 3 подсказки\n'
          '- каждая подсказка уменьшает количество баллов\n'
          '- правильные ответы увеличивают количество баллов')
    print('-' * 60)


if __name__ == '__main__':

    quiz = Questions()
    quiz.load_db(settings['QUIZ_DB'])
    quiz.save_db()
    if quiz.check_save():
        select = ''
        while select not in ('y', 'n'):
            select = input('Load save? y/n')
            if select == 'y':
                quiz.load_db(settings['SAVE_DB'])
            elif select == 'n':
                quiz.load_db(settings['QUIZ_DB'])
    else:
        quiz.load_db(settings['QUIZ_DB'])

    '''play_game = True

    while play_game:
        start_screen()

        questions = load_db(select_db(check_db_save()))
        points = int(questions[0][0])
        record = int(questions[0][1])
        del questions[0]
        save_db(questions)

        play_round = True

        while play_round:
            question = choice(questions)
            cost = WIN_PRICE + len(question[1])

            status_screen()

            if check_answer(question[1]):
                print(f'\nПравильно, "{question[1]}". Вы заработали {cost}✪.')
                points += cost
            else:
                print(
                    f'\nВы не угадали правильный ответ - "{question[1]}" и потеряли {cost}✪.')
                points -= cost

            del questions[questions.index(question)]

            if points > record:
                record = points

            save_db(questions)'''
