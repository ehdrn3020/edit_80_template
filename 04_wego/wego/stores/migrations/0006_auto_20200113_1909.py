# Generated by Django 2.2.2 on 2020-01-13 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0005_store_main_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='image1',
            new_name='pimg1',
        ),
    ]
