# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from varlet import named_urls
from varlet.views_drf import PageViewSet
from varlet import get_version
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter


apiv1 = DefaultRouter()
apiv1.include_format_suffixes = False
apiv1.register(r'pages', PageViewSet)


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include(apiv1.urls)),
    url(r'^page/{version}/'.format(version=get_version()),
        include(named_urls)),
    url(r'^$', RedirectView.as_view(permanent=False,
                                    pattern_name='pages:index')),
]
