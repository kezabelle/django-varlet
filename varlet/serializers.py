from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Page


class ReducedContentTypeSerializer(serializers.ModelSerializer):

    def get_name(self, obj):
        return obj.name

    class Meta:
        model = ContentType
        fields = ['pk', 'name']


class FullContentTypeSerializer(ReducedContentTypeSerializer):
    class Meta(ReducedContentTypeSerializer.Meta):
        fields = ['pk', 'app_label', 'model', 'name']


class PageSerializer(serializers.HyperlinkedModelSerializer):
    object_url = serializers.HyperlinkedIdentityField(view_name='pages:view', lookup_field='slug')
    template = serializers.ChoiceField(choices=())
    possible_templates = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(PageSerializer, self).__init__(*args, **kwargs)
        if 'template' in self.fields:
            self.fields['template'].choices = self.Meta.model.get_template_choices()  # noqa

    def get_possible_templates(self, obj):
        return obj.get_possible_templates()

    def get_content_type(self, obj):
        return self.Meta.content_type_serializer(
            instance=ContentType.objects.get_for_model(obj),
            context=self.context).data

    class Meta:
        content_type_serializer = ReducedContentTypeSerializer
        model = Page
        fields = ['created', 'modified', 'url', 'object_url', 'is_homepage',
                  'title', 'menu_title', 'slug', 'template',
                  'possible_templates', 'content_type']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
        }
