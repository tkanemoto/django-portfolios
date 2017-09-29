# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from ordered_model.admin import OrderedTabularInline, OrderedModelAdmin

from .models import *


class CustomTextAreaSizeMixin(object):
    custom_textarea_rows = 4
    custom_textarea_cols = 85

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(CustomTextAreaSizeMixin, self).formfield_for_dbfield(db_field, **kwargs)
        if isinstance(db_field, models.TextField):
            field.widget.attrs.update({
                'cols': self.custom_textarea_cols,
                'rows': self.custom_textarea_rows,
                'class': ''})
        return field


class PostInline(CustomTextAreaSizeMixin, admin.StackedInline):
    model = Post
    extra = 1


class EmbeddedContentInline(CustomTextAreaSizeMixin, OrderedTabularInline):
    model = EmbeddedContent
    fields = ('content', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ('order',)


class ProjectInline(CustomTextAreaSizeMixin, OrderedTabularInline):
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


class TestimonialInline(CustomTextAreaSizeMixin, OrderedTabularInline):
    model = Testimonial
    fields = ('author', 'title', 'body', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ('order',)
    custom_textarea_rows = 2
    custom_textarea_cols = 60

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'author':
            if not request.user.is_superuser:
                kwargs['queryset'] = db_field.remote_field.model._default_manager.filter(owner=request.user)
        return super(TestimonialInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class SocialMediaLinkInline(OrderedTabularInline):
    model = SocialMediaLink
    fields = ('kind', 'url', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ('order',)


class MemberInline(CustomTextAreaSizeMixin, OrderedTabularInline):
    model = Member
    fields = ('name', 'roles', 'description', 'mugshot', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ('order',)
    custom_textarea_rows = 4
    custom_textarea_cols = 60


class EventInline(CustomTextAreaSizeMixin, admin.StackedInline):
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
        fs = ['slug', 'owner', 'keywords', 'template', 'domain']
        if obj.template == 'band':
            fs += ['showreel', 'clients', 'number_of_featured_clients', 'quote', 'quote_citation', 'quote_background', 'address']
        return fs

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
