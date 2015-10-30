from rest_framework import serializers
from .models import Page


class PageSerializer(serializers.HyperlinkedModelSerializer):
    object_url = serializers.HyperlinkedIdentityField(view_name='pages:view', lookup_field='slug')
    template = serializers.ChoiceField(choices=())
    possible_templates = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):

        super(PageSerializer, self).__init__(*args, **kwargs)
        if 'template' in self.fields:
            self.fields['template'].choices = self.Meta.model.get_template_choices()  # noqa

    def get_possible_templates(self, obj):
        return obj.get_possible_templates()

    class Meta:
        model = Page
        fields = ['created', 'modified', 'url', 'object_url', 'is_homepage',
                  'title', 'menu_title', 'slug', 'template',
                  'possible_templates']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
        }
