from rest_framework import viewsets, mixins, response
from django_filters.rest_framework import DjangoFilterBackend

from .. import serializers

from apps.transactions.models import Category


class CategoryViewSet(
        mixins.UpdateModelMixin,
        viewsets.ReadOnlyModelViewSet
):

    lookup_value_regex = '\d+'

    serializer_class = serializers.CategorySerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ["type"]

    def get_queryset(self):
        if self.action in ['retrieve', 'partial_update', 'update']:
            return Category.objects.all()

        res = (
            Category.objects.filter()
            .prefetch_related('transaction_set')
            .prefetch_related('descriptioninfo_set')
            .order_by('order')
        )

        return res
