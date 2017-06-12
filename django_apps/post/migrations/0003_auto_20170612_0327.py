# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-12 03:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20170612_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like_users',
            field=models.ManyToManyField(related_name='like_post', through='post.PostLike', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterModelTable(
            name='postlike',
            table='post_post_like_users',
        ),
    ]
