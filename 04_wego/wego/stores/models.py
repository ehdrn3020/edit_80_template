from django.db import models
from datetime import datetime
from accounts.models import User

class Store(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    pimg1 = models.CharField(max_length=100, default="NONE")
    item_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    url_link = models.CharField(max_length=200, blank=True)

    click_number = models.IntegerField(default=0)
    best_published = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title

# 쇼핑 메인슬라이드
class Store_Main(models.Model):
    title = models.CharField(max_length=200)
    main = models.ImageField(upload_to='stores/', blank=True)
    main_size = models.CharField(max_length=100, default='826*321')
    sub = models.ImageField(upload_to='stores/', blank=True)
    sub_size = models.CharField(max_length=100, default='543*96')
    link_url = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    click_number = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now, blank=True)
    expiration_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title
