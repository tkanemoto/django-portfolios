# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from ordered_model.models import OrderedModel


UPLOAD_FOLDER = 'uploads/%Y-%m-%d/'
RE_YOUTUBE_ANY = r'^https?://.*youtu\.?be'
RE_YOUTUBE_FULL = r'^https?://.*youtube\.com/watch\?v=([^&]+).*$'
RE_YOUTUBE_EMBED = r'^https?://.*youtube\.com/embed/([^?]+).*$'
RE_YOUTUBE_SHORTENED = r'https?://youtu\.be/([^?]+).*$'
RE_YOUTUBE_REPLACEMENT_EMBED = r'https://www.youtube.com/embed/\1'
RE_YOUTUBE_REPLACEMENT_NORMAL = r'https://www.youtube.com/watch?v=\1'


class Page(models.Model):
    TEMPLATES = (
        ('composer', 'Composer'),
        ('band', 'Band'),
    )
    slug = models.SlugField('slug')
    owner = models.ForeignKey('auth.User', null=True)
    title = models.CharField('title', max_length=100, null=True, help_text='Title text to display')
    subtitle = models.CharField('subtitle', max_length=200, null=True, help_text='Text to display below the title')
    description = models.CharField('description', max_length=400, null=True, blank=True, help_text='Short description for search engines')
    showreel = models.FileField(null=True, blank=True, upload_to=UPLOAD_FOLDER, help_text='The showreel file')
    youtube_playlist = models.CharField(max_length=100, blank=True, null=True, help_text='ID of the YouTube playlist, e.g. PLjZN_n5TZFcxOHUG3TTDbAe4Z_Qz6SuTw')
    about = models.TextField('about', max_length=1000, null=True, blank=True, help_text='Text shown in the About section')
    about_background = models.ImageField(blank=True, null=True, upload_to=UPLOAD_FOLDER)
    mugshot = models.ImageField(null=True, blank=True, upload_to=UPLOAD_FOLDER, help_text='Your profile picture shown in the About section')
    quote = models.TextField('quote', max_length=1000, null=True, blank=True, help_text='Something profound')
    quote_citation = models.CharField('quote citation', max_length=20, null=True, blank=True, help_text='Some profound person')
    quote_background = models.ImageField(blank=True, null=True, upload_to=UPLOAD_FOLDER)
    clients = models.ManyToManyField('Client', blank=True, help_text='Select the clients you would like to be listed in the Credits section')
    number_of_featured_clients = models.IntegerField('number of featured clients', default=5, help_text='The number of clients to show in the big carousel')
    footer_background = models.ImageField(blank=True, null=True, upload_to=UPLOAD_FOLDER)
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

    def __unicode__(self):
        return '{} {}'.format(self.title, self.description if self.description is not None else '')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('portfolios-page', kwargs={'slug': self.slug})

    def featured_clients(self):
        return self.clients.all().filter(order__lt=self.number_of_featured_clients)

    def non_featured_clients(self):
        return self.clients.all().filter(order__gte=self.number_of_featured_clients)

    def roles(self):
        return set(self.clients.all().values_list('project__roles__name', flat=True))

    def products(self):
        return set(self.clients.all().values_list('project__roles__product', flat=True))

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


class EmbeddedContent(OrderedModel):
    content = models.TextField(max_length=1000, help_text='Paste in the embedded content from SoundCloud / YouTube etc.')
    page = models.ForeignKey('Page')
    order_with_respect_to = 'page'

    def __unicode__(self):
        if 'soundcloud.com/player' in self.content:
            return 'SoundCloud track'
        if 'bandcamp.com' in self.content:
            return 'BandCamp album'
        return 'Embedded content'


class Client(OrderedModel):
    name = models.CharField('name', max_length=100, help_text='Name of the client')
    description = models.CharField('description', max_length=200, help_text='Job title or the type of organisation')
    background = models.ImageField(null=True, blank=True, upload_to=UPLOAD_FOLDER, help_text='Background image to display in the carousel')
    mugshot = models.ImageField(null=True, blank=True, upload_to=UPLOAD_FOLDER, help_text='Profile picture')
    showreel_url = models.URLField('showreel URL', blank=True, null=True, help_text='The embedded video URL that best represent the work you\'ve done for this client')
    link = models.URLField(null=True, blank=True, help_text='Link to this client\'s website.')
    owner = models.ForeignKey('auth.User', blank=True)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return '{}'.format(self.name)

    def roles(self):
        return set(self.project_set.all().values_list('roles__name', flat=True))

    def products(self):
        return set(self.project_set.all().values_list('roles__product', flat=True))

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


class Role(models.Model):
    name = models.CharField('name', max_length=20)
    product = models.CharField('product', max_length=20)

    def __unicode__(self):
        return '{}'.format(self.name)


class Project(OrderedModel):
    client = models.ForeignKey('Client')
    name = models.CharField('name', max_length=100)
    roles = models.ManyToManyField('Role')
    category = models.CharField('category', max_length=30)
    date = models.CharField('date', max_length=20)
    url = models.URLField('URL', blank=True, null=True, help_text='URL of the embedded video content')
    order_with_respect_to = 'client'

    def __unicode__(self):
        return '{}'.format(self.name)

    def role_names(self):
        return set(self.roles.all().values_list('name', flat=True))

    def products(self):
        return set(self.roles.all().values_list('product', flat=True))


class Testimonial(OrderedModel):
    author = models.ForeignKey('Client')
    title = models.CharField('title', max_length=200)
    body = models.TextField('body', blank=True)
    page = models.ForeignKey('Page', null=True)
    order_with_respect_to = 'page'

    def __unicode__(self):
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
    )
    kind = models.CharField('kind', max_length=20, choices=SERVICES)
    url = models.URLField('URL')
    page = models.ForeignKey('Page')
    order_with_respect_to = 'page'

    def get_svg_path(self):
        return 'img/{}.svg'.format(self.kind)


class Post(models.Model):
    title = models.CharField('title', max_length=200)
    text = models.TextField('text', max_length=1000)
    link = models.URLField('link', blank=True, null=True)
    link_text = models.CharField('link text', max_length=20, blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to=UPLOAD_FOLDER)
    embedded_content = models.TextField(max_length=400, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    page = models.ForeignKey('Page')

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        return '{}'.format(self.title)


class Member(OrderedModel):
    name = models.CharField('name', max_length=100, help_text='Name of the member')
    roles = models.CharField('roles', max_length=60)
    description = models.TextField('description', blank=True, null=True, max_length=200, help_text='Description')
    mugshot = models.ImageField(null=True, blank=True, upload_to=UPLOAD_FOLDER, help_text='Profile picture')
    page = models.ForeignKey('Page')
    order_with_respect_to = 'page'

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return '{}'.format(self.name)


class Event(models.Model):
    name = models.CharField('event title', max_length=200)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200)
    map_link = models.URLField(blank=True, null=True)
    description = models.TextField(max_length=600, null=True, blank=True)
    link = models.URLField(blank=True, null=True)
    link_text = models.CharField(max_length=20, blank=True, null=True)
    page = models.ForeignKey('Page')

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        return '{}'.format(self.name)
