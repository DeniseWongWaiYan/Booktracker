# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-29 16:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0009_books_total_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='books',
            name='challengebooklist',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='book_in_challenge',
        ),
        migrations.AddField(
            model_name='challenge',
            name='bookinchallenge',
            field=models.ManyToManyField(to='Books.Books'),
        ),
        migrations.AlterField(
            model_name='books',
            name='total_likes',
            field=models.PositiveIntegerField(db_index=True),
        ),
    ]
