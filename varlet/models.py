# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import BooleanField, CharField
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import TimeStampedModel

@python_2_unicode_compatible
class MinimalPage(TimeStampedModel):
    title = CharField(max_length=255, verbose_name=_('title'))
    menu_title = CharField(max_length=255, blank=True,
                           verbose_name=_('menu title'),
                           help_text=_('may be displayed in menus, instead of '
                                       'the standard title'))
    is_homepage = BooleanField(default=False, db_index=True)

    def get_menu_title(self):
        """ utility method for `django CMS`_ api compatibility

        :return: the `menu_title`, or if not set, the `title`
        :rtype: unicode string
        """
        if self.menu_title:
            return self.menu_title
        return self.title

    def get_page_title(self):
        """
        .. note::
            this method is so named to provide API familiarity and compatibility
            with django CMS, of which I am a big proponent.
        """
        return self.title

    def __str__(self):
        return self.title

    @staticmethod
    def _get_template_choices():
        msg = ("Concrete (non-abstract) classes should implement this to "
               "return a list of 2-tuples, representing `template name` "
               "and `display value` for forms.")
        raise NotImplementedError(msg)

    def get_template_names(self):
        """
        Should you wish to override the user's template selection, say to
        interpolate them to use PK-specific ones or something, here's the
        place you'd do it. Used by the detail view to render a page.

        :return: a set of templates to choose from
        :rtype: list of strings
        """
        msg = ("Concrete (non-abstract) classes should implement this to "
               "return a list of template paths that may be discovered by "
               "the Django `TEMPLATE_LOADERS`")
        raise NotImplementedError(msg)

    class Meta:
        abstract = True
