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
    # profile_image = 
    level = models.IntegerField(default=1)
    # level_icon =

    def __str__(self):
        return self.username
