# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-27 11:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_post_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='search_word',
        ),
    ]