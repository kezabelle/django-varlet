from rest_framework import serializers
from .models import Page


class PageSerializer(serializers.HyperlinkedModelSerializer):
    object_url = serializers.HyperlinkedIdentityField(view_name='pages:view')
    template = serializers.ChoiceField(choices=Page.get_template_choices())
    possible_templates = serializers.SerializerMethodField('get_possible_templates')

    def get_possible_templates(self, obj):
        return obj.get_possible_templates()

    class Meta:
        model = Page
        fields = ['created', 'modified', 'url', 'object_url', 'is_homepage',
                  'title', 'menu_title', 'slug', 'template', 'possible_templates']
