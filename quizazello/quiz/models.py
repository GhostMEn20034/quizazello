from django.db import models


class Quiz(models.Model):
    question = models.TextField()
    answer = models.CharField(max_length=200)