# Generated by Django 2.2.2 on 2019-06-17 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='position_1',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='position_2',
        ),
    ]