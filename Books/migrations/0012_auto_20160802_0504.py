# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-02 05:04
from __future__ import unicode_literals

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0011_books_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='photo',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='authors/%y'),
        ),
    ]