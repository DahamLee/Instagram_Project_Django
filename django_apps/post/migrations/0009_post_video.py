# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-27 07:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_auto_20170627_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='post.Video'),
        ),
    ]
