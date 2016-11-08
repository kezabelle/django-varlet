# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import swapper
from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic import DetailView


class Page404(Http404): pass


class PageDetail(DetailView):
    slug_url_kwarg = 'remaining_path'
    slug_field = 'url'

    @property
    def model(self):
        return swapper.load_model("varlet", "Page")

    def get_template_names(self):
        return self.object.get_template_names()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg, None)
        if slug is not None:
            slug = slug.strip('/')
            slug_field = self.get_slug_field()
            query = {slug_field: slug}
            queryset = queryset.filter(**query)
        else:
            raise AttributeError("Missing 'slug_url_kwarg' from self.kwargs")

        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Page404(_(u"No %(verbose_name)s found matching query: %(query)r") %
                          {'verbose_name': queryset.model._meta.verbose_name, 'query': query})
        return obj


page_detail = PageDetail.as_view()
