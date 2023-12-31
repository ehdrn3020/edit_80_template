# Generated by Django 2.2.2 on 2019-11-28 13:51

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
        ('infos', '0001_initial'),
        ('promotions', '0001_initial'),
        ('asks', '0001_initial'),
        ('afters', '0001_initial'),
        ('gallerys', '0001_initial'),
        ('communitys', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment_Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('is_declarated', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=True)),
                ('upload_date', models.DateTimeField(default=datetime.datetime.now)),
                ('comment_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='promotions.Promotion')),
                ('parent_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.Comment_Promotion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('is_declarated', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=True)),
                ('upload_date', models.DateTimeField(default=datetime.datetime.now)),
                ('comment_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infos.Info')),
                ('parent_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.Comment_Info')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment_Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('is_declarated', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=True)),
                ('upload_date', models.DateTimeField(default=datetime.datetime.now)),
                ('comment_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallerys.Gallery')),
                ('parent_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.Comment_Gallery')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment_Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('is_declarated', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=True)),
                ('upload_date', models.DateTimeField(default=datetime.datetime.now)),
                ('comment_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
                ('parent_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.Comment_Course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment_Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('is_declarated', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=True)),
                ('upload_date', models.DateTimeField(default=datetime.datetime.now)),
                ('comment_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='communitys.Community')),
                ('parent_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.Comment_Community')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment_Ask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('is_declarated', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=True)),
                ('upload_date', models.DateTimeField(default=datetime.datetime.now)),
                ('comment_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asks.Ask')),
                ('parent_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.Comment_Ask')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment_After',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('is_declarated', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=True)),
                ('upload_date', models.DateTimeField(default=datetime.datetime.now)),
                ('comment_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='afters.After')),
                ('parent_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.Comment_After')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
