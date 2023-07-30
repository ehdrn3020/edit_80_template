from django.db import models
from datetime import datetime

# 스쿨퀴즈 참가자DB
class SchoolQuiz(models.Model):
    username = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    get_point = models.IntegerField(default=0)
    apply_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title

# 스쿨룰렛 참가자DB
class SchoolRoulette(models.Model):
    username = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    get_point = models.IntegerField(default=0)
    apply_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title