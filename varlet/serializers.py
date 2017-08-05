# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import swapper
from django.contrib.contenttypes.models import ContentType
from rest_framework.fields import ReadOnlyField, SkipField
from rest_framework.serializers import ModelSerializer


class BasePageSerializer(ModelSerializer):
    class Meta:
        fields = (
            'pk', 'url', 'created', 'modified', 'get_absolute_url',
        )
        read_only_fields = (
            'get_absolute_url',
        )


class ContentTypeSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(ContentTypeSerializer, self).__init__(*args, **kwargs)
        self.read_only = True
        self.default = self.fakery

    def fakery(self, *args, **kwargs):
        assert getattr(self.parent.Meta, "model", None) is not None, (
            "The ContentType serializer can only be used on a "
            "ModelSerializer subclass"
        )
        return self.Meta.model.objects.get_for_model(self.parent.Meta.model)

    def validate_empty_values(self, data):
        raise SkipField("This is just a representation")

    class Meta:
        model = ContentType
        fields = ("pk", "app_label", "model", "name")
        read_only_fields = ("pk", "app_label", "model", "name")


class PageSerializer(BasePageSerializer):
    content_type = ContentTypeSerializer()
    template_title = ReadOnlyField(source="get_template_display")

    class Meta(BasePageSerializer.Meta):
        model = swapper.load_model('varlet', 'Page')
        fields = BasePageSerializer.Meta.fields + ("template", "template_title", "content_type")
