from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.settings import api_settings
from .serializers import PageSerializer
from .models import Page


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    lookup_field = 'slug'
    paginate_by = api_settings.PAGINATE_BY or 10
    paginate_by_param = api_settings.PAGINATE_BY_PARAM or 'page'


class SaferPageViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    queryset = PageViewSet.queryset
    serializer_class = PageViewSet.serializer_class
    lookup_field = PageViewSet.lookup_field
    paginate_by = PageViewSet.paginate_by
    paginate_by_param = PageViewSet.paginate_by_param
