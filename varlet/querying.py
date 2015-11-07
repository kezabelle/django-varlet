from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet


class MinimalPageQuerySet(QuerySet):
    def get_homepage(self):
        return self.get(is_homepage=True)

    def not_homepage(self):
        return self.filter(is_homepage=False)



class PageQuerySet(MinimalPageQuerySet):
    def create_page(self, title, template, slug):
        possible_templates = tuple(self.model.get_template_choices())
        if template not in possible_templates:
            raise ValidationError("Invalid template")
        return self.create(title=title, template=template, slug=slug)

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

