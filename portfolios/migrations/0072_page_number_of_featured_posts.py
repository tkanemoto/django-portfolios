# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-09 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0071_auto_20180908_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='number_of_featured_posts',
            field=models.IntegerField(default=5, help_text='Select the number of news posts you would like to be listed in the news section.', verbose_name='number of featured news posts'),
        ),
    ]
