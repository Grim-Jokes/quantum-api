from django.db.models import Prefetch

from rest_framework import viewsets
from apps.transactions.models import Transaction, Category
from . import serializers


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = serializers.TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.all()


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = serializers.SubCategorySerializer

    def get_queryset(self):
        res = Category.objects.filter(
            parent_category=None
        ).select_related('parent_category')

        return res
