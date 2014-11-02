# -*- coding: utf-8 -*-
from haystack.constants import Indexable
from haystack.fields import CharField
from haystack.indexes import SearchIndex
from .models import Page


class MinimalPageIndex(SearchIndex):

    text = CharField(document=True, use_template=True)
    title = CharField(model_attr='title')


class PageIndex(MinimalPageIndex, Indexable):
    get_absolute_url = CharField(model_attr='get_absolute_url')
    created_by = CharField()
    edited_by = CharField()

    def prepare_created_by(self, obj):
        author = obj.author()
        if author.is_anonymous:
            return ''
        return author.get_full_name()

    def prepare_edited_by(self, obj):
        editor = obj.editor()
        if editor.is_anonymous:
            return ''
        return editor.get_full_name()

    def get_model(self):
        return Page

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
