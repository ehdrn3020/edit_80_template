from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Nick Name
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=200)
    # Add Column
    social_login = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    kakaotalk = models.CharField(max_length=100, blank=True)
    point = models.IntegerField(default=100)
    cash = models.IntegerField(default=0)
    profile_image = models.CharField(max_length=100, default="/media/mypages/profiles/profile_img_1.jpg")
    level = models.IntegerField(default=1)
    level_icon = models.CharField(max_length=100, default="/media/mypages/levels/level1.png")
    kind = models.CharField(max_length=100, blank=True) #정회원/블랙회원/VIP
    exprience = models.IntegerField(default=0)
    def __str__(self):
        return self.username
