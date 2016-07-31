# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-28 07:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0008_challenge_book_in_challenge'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='total_likes',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
    ]
