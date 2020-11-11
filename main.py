# -*- coding: utf-8 -*-
# Name: ~ Quizazello ~
# About: This script will help you create a quiz
# Author: Igor Markin
# Blog: https://de0.ru
# Email: 9588604@gmail.com
# Version 0.2

import sys
from collections import Counter
from difflib import SequenceMatcher
from random import choice

# Файл сохранений
DB_SAVE_FILE = 'quiz_save.dat'

# Файл с базой данных
DB_FILE = 'quiz_db.dat'

# Точность проверки ответа
ACCURACY = 0.80

# Количества подсказок до проигрыша
COUNT_HINTS = 4

# Базовый бонус за правильный ответ (+ длина слова)
WIN_PRICE = 5


class Quizazello:

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def get_hint(self, move):
        letters = Counter(list(self.answer)).most_common()
        if (' ', 1) in letters:
            letters.remove((' ', 1))
        for i in range(move, len(letters)):
            hint = self.answer.replace(letters[i][0], '*')
        return hint

    def get_list(self):
        return tuple((self.question, self.answer))


def load_db(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as db:
            list_db = []
            for line in db:
                line = line.replace('\n', '').split('|')
                list_db.append(line)
        return list_db
    except FileNotFoundError:
        press_enter('Файл базы данных не найден.')


def save_db(list_db):
    try:
        with open(DB_SAVE_FILE, 'w', encoding='utf-8') as db:
            db.write(f'{points}|{record}')
            for line in list_db:
                db.write('\n' + '|'.join(line))
        return True
    except IOError:
        press_enter('Игру не удалось сохранить.')


def hint(answer, round_num):
    list_answer = Counter(list(answer)).most_common()
    if (' ', 1) in list_answer:
        list_answer.remove((' ', 1))
    for i in range(round_num, len(list_answer)):
        answer = answer.replace(list_answer[i][0], '*')
    return answer


def check_db_save():
    try:
        open(DB_SAVE_FILE, 'r', encoding='utf-8')
    except FileNotFoundError:
        return False
    else:
        return True


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
    ratio_similarity = SequenceMatcher(None, answer.lower(), text.lower()).ratio()
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

    play_game = True

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
                print(f'\nВы не угадали правильный ответ - "{question[1]}" и потеряли {cost}✪.')
                points -= cost

            del questions[questions.index(question)]

            if points > record:
                record = points

            save_db(questions)
