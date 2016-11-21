# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import swapper
from templatefinder.utils import template_choices
from django.contrib import admin


class PageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'templates', 'created', 'modified',)

    def templates(self, obj):
        choices = template_choices(obj.get_template_names())
        templates = (x[1] for x in choices)
        return ", ".join(templates)

    def get_queryset(self, request):
        qs = super(PageAdmin, self).get_queryset(request=request)
        qs = qs.order_by('url')
        return qs

admin.site.register(swapper.load_model('varlet', 'Page'), admin_class=PageAdmin)
