# Generated by Django 2.2.2 on 2019-06-25 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190619_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='realname',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
