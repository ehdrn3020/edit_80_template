# Generated by Django 2.2.2 on 2020-01-23 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0010_promotion_url_click'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='tag1',
            field=models.CharField(blank=True, default='신규', max_length=10),
        ),
    ]
