# Generated by Django 2.2.2 on 2019-11-28 13:51

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
            name='After',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board_kind', models.CharField(max_length=50)),
                ('attribute', models.CharField(default='NONE', max_length=50)),
                ('likes', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('comments', models.IntegerField(default=0)),
                ('index_image1', models.CharField(default='NONE', max_length=100)),
                ('index_image2', models.CharField(default='NONE', max_length=100)),
                ('index_image3', models.CharField(default='NONE', max_length=100)),
                ('index_image4', models.CharField(default='NONE', max_length=100)),
                ('index_image5', models.CharField(default='NONE', max_length=100)),
                ('index_content', models.CharField(max_length=200)),
                ('tag', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField(blank=True)),
                ('g_map1', models.CharField(max_length=100)),
                ('g_map2', models.CharField(max_length=100)),
                ('g_map3', models.CharField(max_length=100)),
                ('g_map4', models.CharField(max_length=100)),
                ('g_map5', models.CharField(max_length=100)),
                ('url_link', models.CharField(blank=True, max_length=200)),
                ('main_published', models.BooleanField(default=False)),
                ('best_published', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=True)),
                ('upload_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('show_ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banners.Banner')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
