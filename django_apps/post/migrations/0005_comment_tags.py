# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-20 05:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20170620_0553'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='tags',
            field=models.ManyToManyField(to='post.Tag'),
        ),
    ]
