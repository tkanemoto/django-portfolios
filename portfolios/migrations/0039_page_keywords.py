# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-11 09:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0038_auto_20170909_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='keywords',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
