from django.db import models
from datetime import datetime

# Create your models here.
class Banner(models.Model):
    title = models.CharField(max_length=200)
    brand_name = models.CharField(max_length=100)
    link_url = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='banners/', blank=True)
    size = models.CharField(max_length=100, blank=True)
    price = models.IntegerField(default=0)
    position_1 = models.IntegerField(default=0)
    position_2 = models.IntegerField(default=0)
    click_number = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now, blank=True)
    expiration_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title
