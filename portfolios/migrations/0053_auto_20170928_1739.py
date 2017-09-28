# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-28 17:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0052_event_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='link_text',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
