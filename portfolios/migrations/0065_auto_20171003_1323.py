# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 13:23
from __future__ import unicode_literals

from django.db import migrations, models
import portfolios.models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0064_page_media_background'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='news_text',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='news section text'),
        ),
        migrations.AlterField(
            model_name='client',
            name='background',
            field=models.ImageField(blank=True, help_text='Background image to display in the carousel', null=True, upload_to=portfolios.models.get_upload_path),
        ),
        migrations.AlterField(
            model_name='client',
            name='mugshot',
            field=models.ImageField(blank=True, help_text='Profile picture', null=True, upload_to=portfolios.models.get_upload_path),
        ),
        migrations.AlterField(
            model_name='member',
            name='mugshot',
            field=models.ImageField(blank=True, help_text='Profile picture', null=True, upload_to=portfolios.models.get_upload_path),
        ),
        migrations.AlterField(
            model_name='page',
            name='about',
            field=models.TextField(blank=True, help_text='Text shown in the About section', max_length=1000, null=True, verbose_name='about section text'),
        ),
        migrations.AlterField(
            model_name='page',
            name='about_background',
            field=models.ImageField(blank=True, null=True, upload_to=portfolios.models.get_upload_path, verbose_name='about section background image'),
        ),
        migrations.AlterField(
            model_name='page',
            name='favicon',
            field=models.ImageField(blank=True, null=True, upload_to=portfolios.models.get_upload_path),
        ),
        migrations.AlterField(
            model_name='page',
            name='footer_background',
            field=models.ImageField(blank=True, null=True, upload_to=portfolios.models.get_upload_path, verbose_name='footer section background image'),
        ),
        migrations.AlterField(
            model_name='page',
            name='media_background',
            field=models.ImageField(blank=True, null=True, upload_to=portfolios.models.get_upload_path, verbose_name='media section background image'),
        ),
        migrations.AlterField(
            model_name='page',
            name='mugshot',
            field=models.ImageField(blank=True, help_text='Your profile picture shown in the About section', null=True, upload_to=portfolios.models.get_upload_path, verbose_name='mugshot or logo'),
        ),
        migrations.AlterField(
            model_name='page',
            name='quote_background',
            field=models.ImageField(blank=True, null=True, upload_to=portfolios.models.get_upload_path),
        ),
        migrations.AlterField(
            model_name='page',
            name='showreel',
            field=models.FileField(blank=True, help_text='The showreel file', null=True, upload_to=portfolios.models.get_upload_path),
        ),
        migrations.AlterField(
            model_name='page',
            name='youtube_playlist',
            field=models.CharField(blank=True, help_text='ID of the YouTube playlist, e.g. PLjZN_n5TZFcxOHUG3TTDbAe4Z_Qz6SuTw', max_length=100, null=True, verbose_name='YouTube playlist ID'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=portfolios.models.get_upload_path),
        ),
    ]
