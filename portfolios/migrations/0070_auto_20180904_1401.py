# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-04 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0069_auto_20180903_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='embedded_content',
            field=models.CharField(blank=True, max_length=4000, null=True),
        ),
    ]
