# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from django.contrib import admin
from django.http import Http404, HttpResponsePermanentRedirect
from django.views.generic.detail import DetailView
from .compat import ModelContext
from .compat import EditRegionResponseMixin
from .models import Page

logger = logging.getLogger(__name__)


class PageDetail(EditRegionResponseMixin, ModelContext, DetailView):
    model = Page
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'page'
    redirect_type = HttpResponsePermanentRedirect

    #: POST is available in case an :class:`~editregions.models.EditRegionChunk`
    #: needs to render and process a form, and raise a
    #: :exc:`~editregions.views.FormSuccess` exception to redirect.
    http_method_names = ['get', 'head', 'post']

    def get(self, request, *args, **kwargs):
        # taken from BaseDetailView
        self.object = self.get_object()
        if self.object.is_homepage:
            return self.redirect()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_template_names(self):
        return self.object.get_template_names()

    def redirect(self, *args, **kwargs):
        url = self.get_redirect_url(*args, **kwargs)
        return self.redirect_type(url)

    def get_redirect_url(self, *args, **kwargs):
        return self.object.get_absolute_url()


class Homepage(EditRegionResponseMixin, ModelContext, DetailView):
    model = Page
    http_method_names = ['get', 'head', 'post']

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get_homepage()

    def get(self, request, *args, **kwargs):
        try:
            return super(Homepage, self).get(request, *args, **kwargs)
        except self.model.DoesNotExist as e:
            if settings.DEBUG:
                urls = (x.get_absolute_url()
                        for x in self.model.objects.only('slug').all())
                ctx = {
                    'verbose_name': self.model._meta.verbose_name,
                    'verbose_name_plural': self.model._meta.verbose_name_plural,
                    'urls': urls,
                    'admin_namespace': admin.site._registry[self.model],
                    'responds_to': (x.upper() for x in self.http_method_names),
                    'settings': settings.SETTINGS_MODULE,
                }
                response = self.render_to_response(context=ctx)
                response.status_code = 404
                return response
            # no URI was found, and we're in a live environment (DEBUG = False)
            # so we instead have to provide a Page Not Found error.
            msg = "No homepage available"
            logger.info(msg)
            raise Http404(msg)

    def get_template_names(self):
        try:
            return self.object.get_template_names()
        except AttributeError as e:
            # self.object was None, which is probably indicitive of the first
            # usage.
            return ['%s/no_homepage.html' % self.model._meta.app_label]


