from django.db.models import Manager
from django.db.models.query import QuerySet


class PageQuerySet(QuerySet):
    def get_homepage(self):
        return self.get(is_homepage=True)

    def not_homepage(self):
        return self.filter(is_homepage=False)


class PageManager(Manager):
    use_for_related_fields = True

    def get_query_set(self):
        return PageQuerySet(self.model, using=self._db)

    def get_queryset(self):
        return PageQuerySet(self.model, using=self._db)

    def get_homepage(self):
        return self.get_queryset().get_homepage()

    def not_homepage(self):
        return self.get_queryset().not_homepage()
