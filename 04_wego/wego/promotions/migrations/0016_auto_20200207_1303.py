# Generated by Django 2.2.2 on 2020-02-07 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0015_promotion_show_ad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='introduction',
            field=models.CharField(blank=True, max_length=60),
        ),
    ]
