# Generated by Django 2.2.2 on 2020-01-13 12:08

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stores', '0003_shopping_shopping_main'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store_Main',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('main', models.ImageField(blank=True, upload_to='stores/')),
                ('main_size', models.CharField(default='826*321', max_length=100)),
                ('sub', models.ImageField(blank=True, upload_to='stores/')),
                ('sub_size', models.CharField(default='543*96', max_length=100)),
                ('link_url', models.CharField(max_length=200)),
                ('click_number', models.IntegerField(default=0)),
                ('is_published', models.BooleanField(default=True)),
                ('upload_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('expiration_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.RenameModel(
            old_name='Shopping',
            new_name='Store',
        ),
        migrations.DeleteModel(
            name='Shopping_Main',
        ),
    ]
