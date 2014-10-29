from django.core.exceptions import ValidationError
from django.db.models import Manager
from django.db.models.query import QuerySet


class MinimalPageQuerySet(QuerySet):
    def get_homepage(self):
        return self.get(is_homepage=True)

    def not_homepage(self):
        return self.filter(is_homepage=False)


class MinimalPageManager(Manager):
    use_for_related_fields = True

    def get_query_set(self):
        return MinimalPageQuerySet(self.model, using=self._db)

    def get_queryset(self):
        return MinimalPageQuerySet(self.model, using=self._db)

    def get_homepage(self):
        return self.get_queryset().get_homepage()

    def not_homepage(self):
        return self.get_queryset().not_homepage()


class PageQuerySet(MinimalPageQuerySet):
    def create_page(self, title, template, slug):
        possible_templates = tuple(self.model._get_template_choices())
        if template not in possible_templates:
            raise ValidationError("Invalid template")
        return self.create(title=title, template=template, slug=slug)


class PageManager(MinimalPageManager):
    def get_query_set(self):
        return PageQuerySet(self.model, using=self._db)

    def get_queryset(self):
        return PageQuerySet(self.model, using=self._db)

    def create_page(self, title, template, slug):
        return self.get_queryset().create_page(title=title, template=template,
                                               slug=slug)
