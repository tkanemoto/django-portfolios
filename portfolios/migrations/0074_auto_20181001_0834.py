# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-01 08:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0073_auto_20181001_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='embedded_content',
            field=models.CharField(blank=True, max_length=16000, null=True),
        ),
    ]