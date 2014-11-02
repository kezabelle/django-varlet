# -*- coding: utf-8 -*-
import logging
from django.contrib import admin
from .models import Page, PageTemplateError
from .forms import PageAdminForm
from .admin_filters import UsedTemplateFilter
try:
    from .checks import PageAdminConfigChecks
except ImportError:
    def PageAdminConfigChecks():
        return True


logger = logging.getLogger(__name__)


class PageAdminConfig(object):
    """
    Admin for our bundled :class:`varlet.models.Page`
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
    list_filter = [
        UsedTemplateFilter,
    ]
    fieldsets = [
        [None, {
            'fields': (('title', 'menu_title'), 'slug', 'is_homepage'),
        }],
        [None, {
            'fields': ('template',),
        }],

    ]

    def is_homepage(self, obj):
        return obj.is_homepage
    is_homepage.boolean = True
    is_homepage.admin_order_field = 'is_homepage'

    def get_prepopulated_fields(self, request, obj=None):
        """ only pre-populate the slug on add, not edit. """
        prepops = super(PageAdminConfig, self).get_prepopulated_fields(request, obj)
        if obj is not None and obj.slug:
            prepops = {}
        return prepops

    def get_readonly_fields(self, request, obj=None):
        """ disable the slug on edit. Good URIs don't change. """
        readonlys = super(PageAdminConfig, self).get_readonly_fields(request, obj)
        if obj is not None and obj.slug:
            readonlys = tuple(readonlys[:]) + ('slug',)
        return readonlys

    def get_editregions_templates(self, obj):
        """ API requirement for ``django-editregions`` """
        try:
            return obj.get_template_names()
        except PageTemplateError:
            return ()

    def get_editregions_template_choices(self, obj):
        """ API requirement for ``django-editregions`` """
        try:
            return tuple(x[0] for x in obj.get_template_choices())
        except AttributeError:
            return ()


class PageAdmin(PageAdminConfig, admin.ModelAdmin):
    checks_class = PageAdminConfigChecks
admin.site.register(Page, PageAdmin)
