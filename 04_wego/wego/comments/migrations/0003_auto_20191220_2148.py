# Generated by Django 2.2.2 on 2019-12-20 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_comment_customercenter_comment_notice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment_customercenter',
            name='comment_table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='centers.CustomerCenter'),
        ),
        migrations.AlterField(
            model_name='comment_notice',
            name='comment_table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='centers.Notice'),
        ),
    ]