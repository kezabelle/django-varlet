# -*- coding: utf-8 -*-
from haystack.constants import Indexable
from haystack.fields import CharField, BooleanField, NgramField
from haystack.indexes import SearchIndex
from .models import Page


class MinimalPageIndex(SearchIndex):

    text = CharField(document=True, use_template=True)
    title = NgramField(model_attr='title')
    is_homepage = BooleanField(model_attr='is_homepage')
    get_absolute_url = CharField(model_attr='get_absolute_url')


class PageIndex(MinimalPageIndex, Indexable):
    slug = CharField(model_attr='slug')
    template = CharField(model_attr='template', indexed=False)
    created_by = CharField()
    edited_by = CharField()

    def prepare_created_by(self, obj):
        author = obj.author()
        if author.is_anonymous():
            return ''
        return author.get_full_name().strip() or getattr(author, author.USERNAME_FIELD)

    def prepare_edited_by(self, obj):
        editor = obj.editor()
        if editor.is_anonymous():
            return ''
        return editor.get_full_name().strip() or getattr(editor, editor.USERNAME_FIELD)

    def get_model(self):
        return Page

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
