# -*- coding: utf-8 -*-
import logging
from django.db.models.signals import pre_save
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import BooleanField, CharField, SlugField
from django.utils.encoding import python_2_unicode_compatible
from django.template import TemplateDoesNotExist
from model_utils.models import TimeStampedModel
from templatefinder.utils import find_all_templates
from .utils import template_choices
from .listeners import maybe_update_homepage
from .querying import PageManager


logger = logging.getLogger(__name__)


class PageTemplateError(TemplateDoesNotExist):
    pass


@python_2_unicode_compatible
class MinimalPage(TimeStampedModel):
    title = CharField(max_length=255, verbose_name=_('title'))
    menu_title = CharField(max_length=255, blank=True,
                           verbose_name=_('menu title'),
                           help_text=_('may be displayed in menus, instead of '
                                       'the standard title'))
    is_homepage = BooleanField(default=False, db_index=True)
    objects = PageManager()

    def get_menu_title(self):
        """ familiar django-CMS api """
        if self.menu_title:
            return self.menu_title
        return self.title

    def get_page_title(self):
        """ familiar django-CMS api """
        return self.title

    def get_title(self):
        """ familiar django-CMS api """
        return self.title

    def __str__(self):
        return self.title

    @staticmethod
    def get_template_choices():
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
    slug = SlugField(unique=True, db_index=True, max_length=255,
                     verbose_name=_('friendly URL'),
                     help_text=_('a human and search engine friendly '
                                 'name for this object. Only mixed '
                                 'case letters, numbers and dashes are '
                                 'allowed. Once set, this cannot be '
                                 'changed.'))
    template = CharField(max_length=255, db_index=True,
                         verbose_name=_('template'),
                         help_text=_('templates may affect the display '
                                     'of this page on the website.'))

    def get_absolute_url(self):
        if self.is_homepage:
            return reverse('pages:index')
        return reverse('pages:view', kwargs={'slug': self.slug})

    @staticmethod
    def get_template_choices():
        """ For editregions forms ... """
        layout_dir = 'varlet/pages/layouts/*.html'
        return template_choices(find_all_templates(pattern=layout_dir))

    def get_template_names(self):
        """ For editregions """
        if not self.template:
            raise PageTemplateError("No template set ...")
        return (self.template,)

    def get_canonical_slug(self):
        """
        django-braces CanonicalSlugDetailMixin supporting method
        """
        return self.slug

    def _get_logentries(self, *args, **kwargs):
        """
        Find admin log entries pertaining to this model instance
        """
        ct = ContentType.objects.get_for_model(self).pk
        return (LogEntry.objects.filter(content_type_id=ct,
                                        object_id=self.pk)
                .filter(*args, **kwargs)
                .select_related('user')
                .order_by('-action_time'))

    def _get_best_logentry_user(self, *args, **kwargs):
        """
        Ask for just one log entry, matching *args and **kwargs
        as a LogEntry filter
        """
        if self._state.adding:
            return AnonymousUser()
        lazy_entries = self._get_logentries(*args, **kwargs)
        evaluated_entries = tuple(lazy_entries[:1])
        try:
            user = evaluated_entries[0].user
            # user might be None under 1.4 rather than raising DoesNotExist.
            if user is None:
                return AnonymousUser()
            return user
        except IndexError:
            logger.debug('Log entry not found for %r' % self)
            return AnonymousUser()
        except ObjectDoesNotExist:
            logger.debug('User not found for the log entry for %r' % self)
            return AnonymousUser()

    def editor(self):
        """
        Returns the last user whose change was recorded in the admin log,
        or anonymous user if none exist, or the user no longer exists.

        If the model instance has not yet been saved into the database,
        it'll return an anonymous user.

        Other exceptions will bubble up.
        """
        adds_and_changes = Q(action_flag=ADDITION) | Q(action_flag=CHANGE)
        return self._get_best_logentry_user(adds_and_changes)

    def author(self):
        """
        Returns the first user who added this in the admin log,
        or anonymous user if none exist, or the user no longer exists.

        If the model instance has not yet been saved into the database,
        it'll return an anonymous user.

        Other exceptions will bubble up.
        """
        adds_and_changes = Q(action_flag=ADDITION)
        return self._get_best_logentry_user(adds_and_changes)

    class Meta:
        db_table = 'varlet_page'

pre_save.connect(maybe_update_homepage, sender=Page,
                 dispatch_uid='slugpage_maybe_update_homepage')
