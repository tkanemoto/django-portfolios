# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-28 19:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0055_auto_20170928_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='email_booking',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='email_shop',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
