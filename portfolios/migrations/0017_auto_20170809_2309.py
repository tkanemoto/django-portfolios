# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-09 23:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0016_auto_20170809_2308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='role',
        ),
        migrations.AddField(
            model_name='project',
            name='roles',
            field=models.ManyToManyField(to='portfolios.Role'),
        ),
    ]
