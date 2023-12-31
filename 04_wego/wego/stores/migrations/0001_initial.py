# Generated by Django 2.2.2 on 2019-11-28 13:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('get_point', models.IntegerField(default=0)),
                ('apply_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolRoulette',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('get_point', models.IntegerField(default=0)),
                ('apply_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]
