from django.db import models


class Quiz(models.Model):
    question = models.TextField(
        verbose_name='Вопрос',
        help_text='Напишите текст вопроса',
    )
    answer = models.CharField(
        max_length=200,
        verbose_name='Ответ',
        help_text='Напишите текст ответа',
    )
