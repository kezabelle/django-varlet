# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import swapper
from django.http import Http404
from rest_framework import viewsets
from varlet.serializers import PageSerializer


class Page404(Http404): pass


class BasePageViewSet(viewsets.ModelViewSet):
    page_size = 10
    lookup_field = "url"
    lookup_url_kwarg = "url"
    lookup_value_regex = "[^&<>\"\']*?"

    def is_using_template_renderer(self, request):
        renderer = request.accepted_renderer
        return renderer.format == 'html' and hasattr(renderer, 'get_template_names')

    def list(self, request, *args, **kwargs):
        if self.is_using_template_renderer(request=request):
            view = self.__class__.as_view({'get': 'retrieve'})
            response = view(request, **{self.lookup_url_kwarg: request.path.strip('/')})
            return response
        return super(BasePageViewSet, self).list(request, *args, **kwargs)


class PageViewSet(BasePageViewSet):
    queryset = swapper.load_model('varlet', 'Page').objects.all()
    serializer_class = PageSerializer

    def get_template_names(self):
        return [self.response.data['template']]
