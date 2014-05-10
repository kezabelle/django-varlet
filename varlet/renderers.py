# -*- coding: utf-8 -*-
import logging
from django_medusa.renderers import StaticSiteRenderer
from .models import Page

logger = logging.getLogger(__name__)

class BasePageRenderer(StaticSiteRenderer):
    """
    Abstract hook for third-party app `django-medusa`, to flatten a bunch of 
    URLs into static HTML.
    see: https://github.com/mtigas/django-medusa
    """
    def get_model(self):
        raise NotImplementedError("Provide your model")

    def get_paths(self):
        Klass = self.get_model()
        for page in Klass.objects.all():
            yield self.get_url(obj=page)

    def get_url(self, obj):
        return obj.get_absolute_url()


class PageRenderer(BasePageRenderer):
    """
    Concrete implementation of Pages -> Static HTML via django-medusa.
    see: https://github.com/mtigas/django-medusa
    """
    def get_model(self):
        return Page

renderers = (PageRenderer,)
