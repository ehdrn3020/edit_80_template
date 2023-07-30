from django.db import models
from datetime import datetime

# Create your models here.
class Profile_Image(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='mypages/profiles/', blank=True)
    size = models.CharField(max_length=100, blank=True)
    level = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    click_number = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title
