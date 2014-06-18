from rest_framework import serializers
from rest_framework import pagination
from .models import Page


class PageSerializer(serializers.HyperlinkedModelSerializer):
    object_url = serializers.HyperlinkedIdentityField(view_name='pages:view')
    template = serializers.ChoiceField(choices=Page._get_template_choices())
    possible_templates = serializers.SerializerMethodField('get_possible_templates')

    def get_possible_templates(self, obj):
        for value, key in obj._get_template_choices():
            yield {
                'description': key,
                'path': value,
                'selected': obj.template == value
            }

    class Meta:
        model = Page
        fields = ['created', 'modified', 'url', 'object_url', 'is_homepage',
                  'title', 'menu_title', 'slug', 'template', 'possible_templates']
