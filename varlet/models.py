# -*- coding: utf-8 -*-
import logging
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import BooleanField, CharField
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager
from .utils import template_choices
from .listeners import maybe_update_homepage


logger = logging.getLogger(__name__)


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


class Page(MinimalPage):
    slug = models.SlugField(unique=True, db_index=True, max_length=255,
                            verbose_name=_('friendly URL'),
                            help_text=_('a human and search engine friendly '
                                        'name for this object. Only mixed '
                                        'case letters, numbers and dashes are '
                                        'allowed. Once set, this cannot be '
                                        'changed.'))
    template = models.CharField(max_length=255, db_index=True,
                                verbose_name=_('template'),
                                help_text=_('templates may affect the display '
                                            'of this page on the website.'))
    
    tags = TaggableManager()

    def get_absolute_url(self):
        if self.is_homepage:
            return reverse('pages:index')
        return reverse('pages:view', kwargs={'slug': self.slug})

    @staticmethod
    def _get_template_choices():
        """ For forms ... """
        return template_choices('pages/page/*.html')
                                
    def get_template_names(self):
        """ For editregions """
        return [self.template]

    def get_canonical_slug(self):
        """
        django-braces CanonicalSlugDetailMixin supporting method
        """
        return self.slug

    class Meta:
        db_table = 'varlet_page'

pre_save.connect(maybe_update_homepage, sender=Page,
                 dispatch_uid='slugpage_maybe_update_homepage')
