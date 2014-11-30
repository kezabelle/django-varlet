# -*- coding: utf-8 -*-
import json
from django.core.serializers.json import DjangoJSONEncoder
from nap import rest
from nap.serialiser import ModelSerialiser
from nap.serialiser import Field
from .models import Page


class PageSerialiser(ModelSerialiser):
    object_url = Field(attribute='get_absolute_url')
    # template = ...?
    possible_templates = Field(attribute='get_possible_templates',
                               readonly=True)

    class Meta:
        model = Page
        fields = ['created', 'modified', 'url', 'object_url', 'is_homepage',
                  'title', 'menu_title', 'slug', 'template',
                  'possible_templates']


class PagePublisher(rest.ModelPublisher):
    serialiser = PageSerialiser()

    def dumps(self, data):
        return json.dumps(data, cls=DjangoJSONEncoder, indent=4)
