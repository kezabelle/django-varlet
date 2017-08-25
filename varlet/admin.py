# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import swapper
from django.contrib import admin
from django.db.models import Func, F, Value
from django.db.models.functions import Length


class BasePageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created', 'modified',)

    def get_queryset(self, request):
        qs = super(BasePageAdmin, self).get_queryset(request=request)
        x = Func(
            F('url'),
            Value('/'), Value(''),
            function='REPLACE',
        )
        url_len = Length(F('url'))
        counter = url_len - Length(x)
        qs = qs.annotate(slash_count=counter).order_by('url', 'slash_count')
        return qs


class PageAdmin(BasePageAdmin):
    list_display = ('__str__', "get_template_display", 'created', 'modified')

admin.site.register(swapper.load_model('varlet', 'Page'), admin_class=PageAdmin)
