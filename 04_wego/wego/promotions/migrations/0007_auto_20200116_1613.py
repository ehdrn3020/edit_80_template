# Generated by Django 2.2.2 on 2020-01-16 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0006_auto_20200116_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='g_map4',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='promotion',
            name='g_map5',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
