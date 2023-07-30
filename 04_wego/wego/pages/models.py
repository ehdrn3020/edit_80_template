from django.db import models
from datetime import datetime
from accounts.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# 포인트 룰 관련 모델
class Point(models.Model):
    title = models.CharField(max_length=200)
    point = models.IntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

# 경험치 룰 관련 모델
class Exprience(models.Model):
    title = models.CharField(max_length=200)
    exprience = models.IntegerField()
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

# 좋아요 관련 모델
class AddLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_name = models.CharField(max_length=100)
    content_id = models.IntegerField(default=0)
    comment_id = models.IntegerField(default=0)
    content_title = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now, blank=True)

# 별점 관련 모델
class AddStar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    content_name = models.CharField(max_length=100)
    content_id = models.IntegerField(default=0)
    comment_id = models.IntegerField(default=0)
    content_title = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now, blank=True)

# 스크렙 관련 모델
class AddScrap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    is_active = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.tag

# 파트너쉽 쪽지
class PartnerShip(models.Model):
    contact_info = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    upload_date = models.DateTimeField(default=datetime.now, blank=True)
