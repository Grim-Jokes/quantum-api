from django.db.models import Prefetch

from rest_framework import viewsets, mixins
from apps.transactions.models import Transaction, Category
from . import serializers


class TransactionViewSet(
    mixins.UpdateModelMixin,
    viewsets.ReadOnlyModelViewSet
):
    serializer_class = serializers.TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.all()


class CategoryTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.TransactionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context['count'] = self.get_queryset().count()

        return context

    def get_queryset(self):

        category_pk = self.kwargs['category_pk']

        return Transaction.objects.filter(category_id=category_pk)


class CategoryViewSet(
        mixins.UpdateModelMixin,
        viewsets.ReadOnlyModelViewSet
):

    lookup_value_regex = '\d+'

    serializer_class = serializers.RootCategorySerializer

    def get_queryset(self):
        if self.action in ['retrieve', 'partial_update', 'update']:
            return Category.objects.all().select_related('parent_category')

        p = Prefetch('children', Category.objects.all().order_by('order'))

        res = (
            Category.objects.filter()
            .prefetch_related('transaction_set')
            .prefetch_related(p)
            .order_by('order', 'parent_category')
        )

        return res
