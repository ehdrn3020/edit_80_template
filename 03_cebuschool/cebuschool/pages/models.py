from django.db import models
from datetime import datetime

# 포인트 룰 관련 모델
class Point(models.Model):
    title = models.CharField(max_length=200)
    point = models.IntegerField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.title

# API콜 제한횟수 때문에 저장된 값을 사용하기위한 모델
class ApiData(models.Model):
    title = title = models.CharField(max_length=200)
    last_call = models.DateTimeField(default=datetime.now)
    recall_min = models.IntegerField()
    data_list = models.CharField(max_length=200)  
    data1 = models.CharField(max_length=100, blank=True)
    data2 = models.CharField(max_length=100, blank=True)
    data3 = models.CharField(max_length=100, blank=True)
    data4 = models.CharField(max_length=100, blank=True)
    data5 = models.CharField(max_length=100, blank=True)
    data6 = models.CharField(max_length=100, blank=True)
    data7 = models.CharField(max_length=100, blank=True)
    data8 = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title
