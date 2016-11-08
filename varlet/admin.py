# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import swapper
from django.contrib import admin


class PageAdmin(admin.ModelAdmin):
    pass

admin.site.register(swapper.load_model('varlet', 'Page'), admin_class=PageAdmin)
