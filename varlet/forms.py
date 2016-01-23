import logging
from django.forms.models import ModelForm
from django.db.models import BLANK_CHOICE_DASH
from django.forms.widgets import Select
from .models import Page


logger = logging.getLogger(__name__)


class PageAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PageAdminForm, self).__init__(*args, **kwargs)

        # template may not always be in the form, mostly if using
        # my AdminlinksMixin edit_field form
        if 'template' in self.fields:
            # we may get an AdminTextInputWidget if no choices are defined
            templates = list(self._meta.model.get_template_choices())
            if len(templates) < 1:
                logger.debug('No templates given by {cls!r}'.format(
                    cls=self._meta.model))
            templates = BLANK_CHOICE_DASH + templates
            self.fields['template'].widget = Select(choices=templates)

    class Meta:
        model = Page
        fields = ('title', 'is_homepage', 'slug', 'template')
