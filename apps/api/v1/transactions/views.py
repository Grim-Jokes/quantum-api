from rest_framework import viewsets
from apps.transactions.models import Transaction, Category

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    
    def get_queryset(self):
        return Transaction.objects.all()


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        return Category.objects.all()
    