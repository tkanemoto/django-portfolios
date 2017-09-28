# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from ordered_model.admin import OrderedTabularInline, OrderedModelAdmin

from .models import *


class PostInline(admin.StackedInline):
    model = Post
    extra = 1


class EmbeddedContentInline(OrderedTabularInline):
    model = EmbeddedContent
    fields = ('content', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ('order',)


class ProjectInline(OrderedTabularInline):
    model = Project
    fields = ('client', 'name', 'category', 'roles', 'date', 'url', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ('order',)


class ClientAdmin(OrderedModelAdmin):
    list_display = ('name', 'description', 'order', 'move_up_down_links')
    inlines = [
        ProjectInline
    ]

    def get_urls(self):
        urls = super(ClientAdmin, self).get_urls()
        for inline in self.inlines:
            if hasattr(inline, 'get_urls'):
                urls = inline.get_urls(self) + urls
        return urls

    def get_queryset(self, request):
        qs = super(ClientAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if 'owner' not in form.data or form.data['owner'] is None or form.data['owner'] == '':
            obj.owner = request.user
        super(ClientAdmin, self).save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        if request.user.is_superuser:
            return []
        return ['owner']


class TestimonialInline(OrderedTabularInline):
    model = Testimonial
    fields = ('author', 'title', 'body', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ('order',)


class SocialMediaLinkInline(OrderedTabularInline):
    model = SocialMediaLink
    fields = ('kind', 'url', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ('order',)


class MemberInline(OrderedTabularInline):
    model = Member
    fields = ('name', 'roles', 'description', 'mugshot', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ('order',)


class EventInline(admin.StackedInline):
    model = Event
    extra = 1


class PageAdmin(admin.ModelAdmin):
    inlines = [
        EventInline,
        MemberInline,
        PostInline,
        EmbeddedContentInline,
        TestimonialInline,
        SocialMediaLinkInline,
    ]
    filter_horizontal = ('clients',)

    def get_urls(self):
        urls = super(PageAdmin, self).get_urls()
        for inline in self.inlines:
            if hasattr(inline, 'get_urls'):
                urls = inline.get_urls(self) + urls
        return urls

    def get_queryset(self, request):
        qs = super(PageAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        if request.user.is_superuser:
            return []
        return ['owner', 'keywords', 'template', 'domain']

    def get_field_queryset(self, db, db_field, request):
        """ Only show clients belonging to the owner. """

        if db_field.name == 'clients':
            if not request.user.is_superuser:
                return db_field.remote_field.model._default_manager.filter(owner=request.user)

        return super(PageAdmin, self).get_field_queryset(db, db_field, request)


#admin.site.register(Testimonial)
admin.site.register(Role)
#admin.site.register(Project)
admin.site.register(Client, ClientAdmin)
admin.site.register(Page, PageAdmin)
