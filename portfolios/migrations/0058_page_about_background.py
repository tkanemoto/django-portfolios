# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-28 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0057_page_domain'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='about_background',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/%Y-%m-%d/'),
        ),
    ]
