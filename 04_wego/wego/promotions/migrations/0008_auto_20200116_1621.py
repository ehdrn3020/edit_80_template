# Generated by Django 2.2.2 on 2020-01-16 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0007_auto_20200116_1613'),
    ]

    operations = [
        migrations.RenameField(
            model_name='promotion',
            old_name='title',
            new_name='introduction',
        ),
    ]
