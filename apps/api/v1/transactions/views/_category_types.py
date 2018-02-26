from rest_framework import viewsets, mixins

from apps.transactions.models import CategoryType, Category

from .. import serializers

class FilteredCategories(viewsets.GenericViewSet, mixins.ListModelMixin):

    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        _type = self.kwargs['type']

        _type = CategoryType.objects.get(name__iexact=_type)

        return Category.objects.filter(type=_type)
