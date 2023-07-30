# Generated by Django 2.2.2 on 2019-12-18 15:10

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('banners', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board_kind', models.CharField(max_length=50)),
                ('attribute', models.CharField(default='공지', max_length=50)),
                ('likes', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('comments', models.IntegerField(default=0)),
                ('tag', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField(blank=True)),
                ('url_link', models.CharField(blank=True, max_length=200)),
                ('is_imaged', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=True)),
                ('upload_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerCenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board_kind', models.CharField(max_length=50)),
                ('attribute', models.CharField(default='고객센터', max_length=50)),
                ('likes', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('comments', models.IntegerField(default=0)),
                ('tag', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField(blank=True)),
                ('url_link', models.CharField(blank=True, max_length=200)),
                ('is_imaged', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=True)),
                ('upload_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('show_ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banners.Banner')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]