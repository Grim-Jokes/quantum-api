from rest_framework import viewsets, mixins
from apps.transactions.models import Transaction, Category
from . import serializers


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(cateogry_id=None)


class CategoryTransactionViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = serializers.TransactionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context['count'] = self.get_queryset().count()

        return context

    def get_queryset(self):
        return Transaction.objects.filter(
            category_id=self.kwargs['category_pk']
        )


class CategoryViewSet(
        mixins.UpdateModelMixin,
        viewsets.ReadOnlyModelViewSet):

    lookup_value_regex = '\d+'

    serializer_class = serializers.RootCategorySerializer

    def get_serializer_class(self):
        if self.action in ['retrieve', 'partial_update']:
            return serializers.ChildCategorySerializer
        else:
            return serializers.RootCategorySerializer

    def get_queryset(self):

        if self.action in ['retrieve', 'partial_update', 'update']:
            return Category.objects.all().select_related('parent_category')
        else:
            res = Category.objects.filter(
                parent_category=None
            ).select_related('parent_category')

        return res
