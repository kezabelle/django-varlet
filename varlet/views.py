# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import swapper
from django.conf.urls import url
from rest_framework.viewsets import ModelViewSet
from varlet.serializers import PageSerializer


class BasePageViewSet(ModelViewSet):
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

    @classmethod
    def as_detail_view(cls, **extra_kwargs):
        return cls.as_view(actions={
            'get': 'retrieve',
            'patch': 'partial_update',
            'delete': 'destroy',
            'put': 'update'
        }, suffix="Instance", **extra_kwargs)

    @classmethod
    def as_root_view(cls, **extra_kwargs):
        return PageViewSet.as_view(actions={
            'post': 'create',
            'get': 'list'
        }, suffix="List", **extra_kwargs)

    @classmethod
    def as_detail_url(cls):
        regex = r'^(?P<{lookup_url_kwarg}>{lookup_value})/$'.format(
                lookup_url_kwarg=cls.lookup_url_kwarg,
                lookup_value=cls.lookup_value_regex
        )
        return url(regex=regex, view=cls.as_detail_view(), name='page-detail')

    @classmethod
    def as_root_url(cls):
        return url(r'^$', cls.as_root_view(), name="page-list")


class PageViewSet(BasePageViewSet):
    queryset = swapper.load_model('varlet', 'Page').objects.all()
    serializer_class = PageSerializer

    def get_template_names(self):
        return [self.response.data['template']]
