# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import swapper
from django.contrib import admin


class PageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'templates', 'created', 'modified',)

    def templates(self, obj):
        return ", ".join(obj.get_template_names())

admin.site.register(swapper.load_model('varlet', 'Page'), admin_class=PageAdmin)
