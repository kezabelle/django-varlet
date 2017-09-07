# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import os

import operator
import re
from difflib import SequenceMatcher
from itertools import chain

from django.core.exceptions import ValidationError
try:
    from django.urls import reverse, NoReverseMatch
except ImportError:
    from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.six.moves import reduce, range
from django.http import JsonResponse
from functools import update_wrapper

import swapper
from django.contrib import admin
from django.contrib.admin.widgets import AdminTextInputWidget
from django.db.models import Func, F, Value, Q
from django.db.models.functions import Length
from varlet.models import URLPathField


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

    def get_urls(self):
        urlpatterns = super(BasePageAdmin, self).get_urls()
        from django.conf.urls import url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)
        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            url(r'^urls/$', wrap(self.autocomplete), name='%s_%s_autocomplete' % info),
        ] + urlpatterns
        return urlpatterns

    def autocomplete(self, request, *args, **kwargs):
        error_response = JsonResponse(data={'results': [], 'count': 0}, status=404)
        query = request.GET.get('q', '').strip()
        if not query:
            return error_response
        field = self.model._meta.get_field('url')
        try:
            query2 = field.to_python(query)
        except ValidationError:
            return error_response

        query3 = query2.split("/")
        query4 = tuple("/".join(query3[0:x]) for x in range(1, len(query3)+1))
        if not query4:
            return error_response
        query5 = (Q(url__icontains=x) for x in query4)
        query7 = reduce(operator.or_, query5)

        def sorty(x):
            input_length = len(query2)
            result_length = len(x)
            matcher = SequenceMatcher(None, query2, x)
            longest = matcher.find_longest_match(0, input_length, 0, result_length)
            prefix = os.path.commonprefix([query2, x])
            prefix_length = len(prefix) or -1
            result =  matcher.ratio() + longest.size + prefix_length + result_length
            return result

        data = tuple(self.model.objects
                     .distinct()
                     .values_list('url', flat=True)
                     .exclude(url=query2)
                     .filter(query7)
                     .annotate(url_length=Length('url'))
                     .filter(url_length__gt=len(query2))[0:50]
                     .iterator())
        sorted_data = tuple({'name': obj}
                            for obj in sorted(data, key=sorty, reverse=True))
        return JsonResponse(data={'results': sorted_data[0:12], 'count': len(data)})


class PageAdmin(BasePageAdmin):
    list_display = ('__str__', "get_template_display", 'created', 'modified')


class AdminAutocompleteURLField(AdminTextInputWidget):
    template_name = 'django/forms/widgets/urlpath-autocomplete.html'

    def get_admin_url(self):
        model = swapper.load_model('varlet', 'Page')
        if not admin.site.is_registered(model):
            return None
        try:
            url = reverse('admin:{}_{}_autocomplete'.format(
                model._meta.app_label, model._meta.model_name))
        except NoReverseMatch:
            return None
        return url

    def get_context(self, name, value, attrs):
        context = super(AdminAutocompleteURLField, self).get_context(name, value, attrs)
        url = self.get_admin_url()
        if url is not None:
            context['AUTOCOMPLETE_URL'] = url
        return context

    class Media:
        js = (
            "varlet/riot.min.js",
            "varlet/urlpath-autocomplete.js",
          )
        css = {
            'screen': (
                'varlet/urlpath-autocomplete.css',
            )
        }


admin.options.FORMFIELD_FOR_DBFIELD_DEFAULTS[URLPathField] = {'widget': AdminAutocompleteURLField}
admin.site.register(swapper.load_model('varlet', 'Page'), admin_class=PageAdmin)
