from django.db.models import Prefetch

from rest_framework import viewsets
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
        return Transaction.objects.filter(category_id=self.kwargs['category_pk'])


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = serializers.SubCategorySerializer

    def get_queryset(self):
        res = Category.objects.filter(
            parent_category=None
        ).select_related('parent_category')

        return res
