# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-28 18:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0053_auto_20170928_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='extra_copyright_text',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='socialmedialink',
            name='kind',
            field=models.CharField(choices=[('facebook', 'Facebook'), ('linkedin', 'LinkedIn'), ('twitter', 'Twitter'), ('soundcloud', 'SoundCloud'), ('spotify', 'Spotify'), ('youtube', 'YouTube'), ('github', 'GitHub'), ('bandcamp', 'BandCamp'), ('vevo', 'Vevo'), ('itunes', 'iTunes'), ('lastfm', 'LastFM')], max_length=20, verbose_name='kind'),
        ),
    ]
