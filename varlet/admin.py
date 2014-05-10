# -*- coding: utf-8 -*-
import logging
from django.contrib import admin
from adminlinks.admin import AdminlinksMixin
from editregions.admin import EditRegionInline
from .models import Page, PageTemplateError
from .forms import PageAdminForm
from .compat import ParsleyAdminMixin, SupportsQuickAdd

logger = logging.getLogger(__name__)


class PageAdmin(ParsleyAdminMixin, SupportsQuickAdd, AdminlinksMixin,
                admin.ModelAdmin):
    """
    Admin for our bundled :class:`oranpage.models.Page`
    """
    form = PageAdminForm
    search_fields = ['title', 'menu_title']
    prepopulated_fields = {
        "slug": [
            "title",
        ]
    }
    actions = None
    list_display = [
        'slug',
        'title',
        'is_homepage',
        'modified',
    ]
    fieldsets = [
        [None, {
            'fields': (('title', 'menu_title'), 'slug', 'is_homepage'),
        }],
        [None, {
            'fields': ('template',),
        }],

    ]
    inlines = [
        EditRegionInline,
    ]

    def is_homepage(self, obj):
        return obj.is_homepage
    is_homepage.boolean = True
    is_homepage.admin_order_field = 'is_homepage'

    def get_prepopulated_fields(self, request, obj=None):
        """
        only pre-populate the slug on add, not edit.
        """
        prepops = super(PageAdmin, self).get_prepopulated_fields(request, obj)
        if obj is not None and obj.slug:
            prepops = {}
        return prepops

    def get_readonly_fields(self, request, obj=None):
        """
        disable the slug on edit. Good URIs don't change.
        """
        readonlys = super(PageAdmin, self).get_readonly_fields(request, obj)
        if obj is not None and obj.slug:
            readonlys = tuple(readonlys[:]) + ('slug',)
        return readonlys

    def get_editregions_templates(self, obj):
        """
        API requirement for ``django-editregions``
        """
        try:
            return obj.get_template_names()
        except PageTemplateError:
            return ()
admin.site.register(Page, PageAdmin)
