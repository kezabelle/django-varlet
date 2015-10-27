from django.contrib.admin.filters import SimpleListFilter
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.admin.options import IncorrectLookupParameters
from django.utils.translation import ugettext_lazy as _
from templatefinder.utils import template_choices


class UsedTemplateFilter(SimpleListFilter):
    title = _("template")
    parameter_name = '_template'

    def lookups(self, request, model_admin):
        bad_entries = Q(template=None) | Q(template='')
        templates = tuple(model_admin.model.objects.exclude(bad_entries)
                          .values_list('template', flat=True).distinct())
        templates_sorted = sorted(templates)
        return template_choices(templates=templates_sorted)

    def queryset(self, request, queryset):
        if self.parameter_name in self.used_parameters:
            param = self.used_parameters[self.parameter_name]
            final_qs_val = {'template__exact': param}
            try:
                return queryset.filter(**final_qs_val)
            except ValidationError as e:
                raise IncorrectLookupParameters(e)
        return queryset
