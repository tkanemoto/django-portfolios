# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-12 12:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0034_auto_20170812_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
