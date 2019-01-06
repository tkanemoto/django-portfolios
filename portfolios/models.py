# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os.path
import datetime
import requests

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from ordered_model.models import OrderedModel


UPLOAD_FOLDER = 'uploads/{slug}/{file}'
RE_YOUTUBE_ANY = r'^https?://.*youtu\.?be'
RE_YOUTUBE_FULL = r'^https?://.*youtube\.com/watch\?v=([^&]+).*$'
RE_YOUTUBE_EMBED = r'^https?://.*youtube\.com/embed/([^?]+).*$'
RE_YOUTUBE_SHORTENED = r'https?://youtu\.be/([^?]+).*$'
RE_YOUTUBE_REPLACEMENT_EMBED = r'https://www.youtube.com/embed/\1'
RE_YOUTUBE_REPLACEMENT_NORMAL = r'https://www.youtube.com/watch?v=\1'


def get_upload_path(instance, filename):
    slug = '%Y-%m-%d'
    if hasattr(instance, 'slug'):
        slug = instance.slug
    elif hasattr(instance, 'page'):
        slug = instance.page.slug
    elif hasattr(instance, 'owner'):
        if instance.owner.page_set.all().count() == 1:
            slug = instance.owner.page_set.all()[0].slug
        else:
            slug = instance.owner.username
    return UPLOAD_FOLDER.format(slug=slug, file=filename)


@python_2_unicode_compatible
class Page(models.Model):
    TEMPLATES = (
        ('composer', 'Composer'),
        ('band', 'Band'),
    )
    slug = models.SlugField('slug')
    owner = models.ForeignKey('auth.User', null=True, on_delete=models.SET_NULL)
    title = models.CharField('title', max_length=100, null=True, help_text='Title text to display')
    subtitle = models.CharField('subtitle', max_length=200, null=True, help_text='Text to display below the title')
    description = models.CharField('description', max_length=400, null=True, blank=True, help_text='Short description for search engines')
    showreel = models.FileField(null=True, blank=True, upload_to=get_upload_path, help_text='The showreel file')
    youtube_playlist = models.CharField('YouTube playlist ID', max_length=100, blank=True, null=True, help_text='ID of the YouTube playlist, e.g. PLjZN_n5TZFcxOHUG3TTDbAe4Z_Qz6SuTw')
    about = models.TextField('about section text', max_length=1000, null=True, blank=True, help_text='Text shown in the About section')
    about_background = models.ImageField('about section background image', blank=True, null=True, upload_to=get_upload_path)
    mugshot = models.ImageField('mugshot or logo', null=True, blank=True, upload_to=get_upload_path, help_text='Your profile picture shown in the About section')
    quote = models.TextField('quote', max_length=1000, null=True, blank=True, help_text='Something profound')
    quote_citation = models.CharField('quote citation', max_length=20, null=True, blank=True, help_text='Some profound person')
    quote_background = models.ImageField(blank=True, null=True, upload_to=get_upload_path)
    news_text = models.TextField('news section text', max_length=200, null=True, blank=True)
    number_of_featured_posts = models.IntegerField('number of featured news posts', default=5, help_text='Select the number of news posts you would like to be listed in the news section.')
    clients = models.ManyToManyField('Client', blank=True, help_text='Select the clients you would like to be listed in the Credits section')
    number_of_featured_clients = models.IntegerField('number of featured clients', default=5, help_text='The number of clients to show in the big carousel')
    media_background = models.ImageField('media section background image', blank=True, null=True, upload_to=get_upload_path)
    footer_background = models.ImageField('footer section background image', blank=True, null=True, upload_to=get_upload_path)
    email = models.EmailField(null=True, blank=True, help_text='The email address people should contact you about this page')
    email_booking = models.EmailField(null=True, blank=True)
    email_shop = models.EmailField(null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=20, help_text='The contact phone number')
    address = models.TextField(null=True, blank=True, max_length=300, help_text='Postal address')
    extra_copyright_text = models.TextField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    keywords = models.CharField(null=True, blank=True, max_length=200)
    template = models.CharField('template', max_length=20, choices=TEMPLATES)
    domain = models.CharField(max_length=40)
    favicon = models.ImageField(null=True, blank=True, upload_to=get_upload_path)
    instagram_access_token = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.title, self.description if self.description is not None else '')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('portfolios-page', kwargs={'slug': self.slug})

    def featured_clients(self):
        return self.clients.all().filter(order__lt=self.number_of_featured_clients)

    def non_featured_clients(self):
        return self.clients.all().filter(order__gte=self.number_of_featured_clients)

    def roles(self):
        return sorted(set(self.clients.all().values_list('project__roles__name', flat=True)))

    def products(self):
        return sorted(set(self.clients.all().values_list('project__roles__product', flat=True)))

    def copyright(self):
        if self.date_created.year != self.date_modified.year:
            return u'{} - {}'.format(self.date_created.year, self.date_modified.year)
        return u'{}'.format(self.date_created.year)

    def get_embeddedcontent_url(self):
        if self.embeddedcontent_set.all().exists():
            import re
            m = re.match('<iframe .*src="([^"]+)"', self.embeddedcontent_set.all()[0].content)
            if m:
                return m.group(1)
        return ''

    def get_soundcloud_contents(self):
        return self.get_embeddedcontent_by_kind('soundcloud')

    def get_bandcamp_contents(self):
        return self.get_embeddedcontent_by_kind('bandcamp')

    def get_youtube_contents(self):
        return self.get_embeddedcontent_by_kind('youtube')

    def get_audio_contents(self):
        return self.get_soundcloud_contents() | self.get_bandcamp_contents()

    def get_video_contents(self):
        return self.get_youtube_contents()

    def get_embeddedcontent_by_kind(self, kind):
        return self.embeddedcontent_set.all().filter(kind=kind)

    def get_instagram_posts(self):
        qs = self.socialmedialink_set.all().filter(kind='instagram')
        if qs.exists():
            self.embeddedcontent_set.all().filter(content__contains='instagram-media').delete()
            self.post_set.all().filter(embedded_content__contains='instagram-media').delete()
            account = os.path.basename(qs[0].url.rstrip('/'))
            r = requests.get('https://api.instagram.com/v1/users/self/media/recent/?access_token={}&count=5'.format(self.instagram_access_token))
            if r.status_code == 200 and r.headers['content-type'].startswith('application/json'):
                for post in r.json()['data']:
                    link = post['link']
                    ctime = datetime.datetime.fromtimestamp(int(post['created_time']))
                    text = post['caption']['text'] if post['caption'] else ''
                    text += '<ul class="list-inline">'
                    text += '<li class="list-inline-item"><a href="{}" target="_blank"><i class="fa fa-fw fa-heart"></i> {}</a></li>'.format(link, str(post['likes']['count']))
                    text += '<li class="list-inline-item"><a href="{}" target="_blank"><i class="fa fa-fw fa-comment"></i> {}</a></li>'.format(link, str(post['comments']['count']))
                    text += '</ul>'
                    r2 = requests.get('https://api.instagram.com/oembed/?url={}&omitscript=1&hidecaption=1'.format(link))
                    if r2.status_code == 200 and r2.headers['content-type'].startswith('application/json'):
                        p, _c = Post.objects.get_or_create(title='', text=text, date=ctime, link=link, embedded_content=r2.json()['html'], page=self)
                        p.date = ctime
                        p.save()

        return self.post_set.all().filter(embedded_content__contains='instagram-media')

    def get_posts(self):
        self.get_instagram_posts()
        return self.post_set.all()[:self.number_of_featured_posts]

    def upcoming_events(self):
        qs = self.event_set.all()
        if qs.exists():
            return (qs.filter(date__gte=timezone.now().date()) |
                    qs.filter(date__isnull=True))
        return qs

    def past_events(self):
        qs = self.event_set.all()
        if qs.exists():
            return qs.filter(date__lt=timezone.now().date())
        return qs


@python_2_unicode_compatible
class EmbeddedContent(OrderedModel):
    content = models.TextField(max_length=16000, help_text='Paste in the embedded content from SoundCloud / YouTube etc.')
    SERVICES = (
        ('soundcloud', 'SoundCloud'),
        ('spotify', 'Spotify'),
        ('youtube', 'YouTube'),
        ('bandcamp', 'BandCamp'),
        ('vevo', 'Vevo'),
        ('itunes', 'iTunes'),
        ('lastfm', 'LastFM'),
        ('tumblr', 'Tumblr'),
        ('instagram', 'Instagram'),
    )
    kind = models.CharField('kind', max_length=20, choices=SERVICES, default='embedded')
    thumbnail = models.ImageField('thumbnail', blank=True, null=True, upload_to=get_upload_path)
    page = models.ForeignKey('Page', on_delete=models.CASCADE)
    order_with_respect_to = 'page'

    def __str__(self):
        return '{} content'.format(self.kind)

    def save(self, *args, **kwargs):
        if 'soundcloud.com/player' in self.content:
            self.kind = 'soundcloud'
        elif 'bandcamp.com' in self.content:
            self.kind = 'bandcamp'
        elif 'youtube' in self.content:
            self.kind = 'youtube'
        elif 'spotify' in self.content:
            self.kind = 'spotify'
        elif 'itunes' in self.content:
            self.kind = 'itunes'
        super(EmbeddedContent, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Client(OrderedModel):
    name = models.CharField('name', max_length=100, help_text='Name of the client')
    description = models.CharField('description', max_length=200, help_text='Job title or the type of organisation')
    background = models.ImageField(null=True, blank=True, upload_to=get_upload_path, help_text='Background image to display in the carousel')
    mugshot = models.ImageField(null=True, blank=True, upload_to=get_upload_path, help_text='Profile picture')
    showreel_url = models.URLField('showreel URL', blank=True, null=True, help_text='The embedded video URL that best represent the work you\'ve done for this client')
    link = models.URLField(null=True, blank=True, help_text='Link to this client\'s website.')
    owner = models.ForeignKey('auth.User', blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return '{}'.format(self.name)

    def roles(self):
        return sorted(set(self.project_set.all().values_list('roles__name', flat=True)))

    def products(self):
        return sorted(set(self.project_set.all().values_list('roles__product', flat=True)))

    def _youtube_url(self, url, embed=False):
        import re
        replacement = RE_YOUTUBE_REPLACEMENT_EMBED if embed else RE_YOUTUBE_REPLACEMENT_NORMAL
        for pattern in [RE_YOUTUBE_FULL, RE_YOUTUBE_SHORTENED, RE_YOUTUBE_EMBED]:
            m = re.match(pattern, url)
            if m:
                return re.sub(pattern, replacement, url)
        return url

    def _video_url(self, embed=False):
        if self.showreel_url:
            return self._youtube_url(self.showreel_url, embed)
        elif self.project_set.filter(url__regex=RE_YOUTUBE_ANY).exists():
            p = self.project_set.filter(url__regex=RE_YOUTUBE_ANY)[0]
            return self._youtube_url(p.url, embed)
        return ''

    def video_url(self):
        return self._video_url(embed=False)

    def embed_url(self):
        return self._video_url(embed=True)


@python_2_unicode_compatible
class Role(models.Model):
    name = models.CharField('name', max_length=20)
    product = models.CharField('product', max_length=20)

    def __str__(self):
        return '{}'.format(self.name)


@python_2_unicode_compatible
class Project(OrderedModel):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    name = models.CharField('name', max_length=100)
    roles = models.ManyToManyField('Role')
    category = models.CharField('category', max_length=30)
    date = models.CharField('date', max_length=20)
    url = models.URLField('URL', blank=True, null=True, help_text='URL of the embedded video content')
    order_with_respect_to = 'client'

    def __str__(self):
        return '{}'.format(self.name)

    def role_names(self):
        return sorted(set(self.roles.all().values_list('name', flat=True)))

    def products(self):
        return sorted(set(self.roles.all().values_list('product', flat=True)))


@python_2_unicode_compatible
class Testimonial(OrderedModel):
    author = models.ForeignKey('Client', on_delete=models.CASCADE)
    title = models.CharField('title', max_length=200)
    body = models.TextField('body', max_length=400, null=True, blank=True)
    page = models.ForeignKey('Page', null=True, on_delete=models.CASCADE)
    order_with_respect_to = 'page'

    def __str__(self):
        return '{} : {} "{}"'.format(self.author, self.title, self.body)


class SocialMediaLink(OrderedModel):
    SERVICES = (
        ('facebook', 'Facebook'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
        ('soundcloud', 'SoundCloud'),
        ('spotify', 'Spotify'),
        ('youtube', 'YouTube'),
        ('github', 'GitHub'),
        ('bandcamp', 'BandCamp'),
        ('vevo', 'Vevo'),
        ('itunes', 'iTunes'),
        ('lastfm', 'LastFM'),
        ('tumblr', 'Tumblr'),
        ('instagram', 'Instagram'),
    )
    kind = models.CharField('kind', max_length=20, choices=SERVICES)
    url = models.URLField('URL')
    page = models.ForeignKey('Page', on_delete=models.CASCADE)
    order_with_respect_to = 'page'

    def get_svg_path(self):
        return 'img/{}.svg'.format(self.kind)


@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField('title', max_length=200)
    text = models.TextField('text', max_length=1000)
    link = models.URLField('link', blank=True, null=True)
    link_text = models.CharField('link text', max_length=20, blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to=get_upload_path)
    embedded_content = models.CharField(max_length=16000, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    page = models.ForeignKey('Page', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-date',)
        verbose_name = 'news post'

    def __str__(self):
        return '{}'.format(self.title)


@python_2_unicode_compatible
class Member(OrderedModel):
    name = models.CharField('name', max_length=100, help_text='Name of the member')
    roles = models.CharField('roles', max_length=60)
    description = models.TextField('description', blank=True, null=True, max_length=400, help_text='Description or bio')
    mugshot = models.ImageField(null=True, blank=True, upload_to=get_upload_path, help_text='Profile picture')
    page = models.ForeignKey('Page', on_delete=models.CASCADE)
    order_with_respect_to = 'page'

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return '{}'.format(self.name)


@python_2_unicode_compatible
class Event(models.Model):
    name = models.CharField('event title', max_length=200)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200)
    map_link = models.URLField(blank=True, null=True)
    description = models.TextField(max_length=600, null=True, blank=True)
    link = models.URLField(blank=True, null=True)
    link_text = models.CharField(max_length=20, blank=True, null=True)
    page = models.ForeignKey('Page', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return '{} - {}'.format(self.name, self.date)
