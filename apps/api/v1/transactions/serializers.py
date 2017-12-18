from django.db.models import Sum

from rest_framework import serializers
from apps.transactions.models import Transaction, Category


def get_income(instance):
    return (
        instance.id == 1 or
        instance.parent_category and instance.parent_category_id == 1 or
        instance.parent_category and
        instance.parent_category.parent_category_id == 1
    )


def get_limit(instance):
    if not instance.children.exists():
        return instance.limit
    return 0.0


class TransactionSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='name.name')

    class Meta:
        model = Transaction
        fields = '__all__'


class RootCategorySerializer(serializers.ModelSerializer):

    budget = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source="limit"
    )

    accumulated = serializers.SerializerMethodField()

    def get_accumulated(self, category):
        return (
            category.transaction_set
            .aggregate(total=Sum('value'))
            .get('total', 0.00) or 0.00
        )

    has_transactions = serializers.SerializerMethodField()

    def get_has_transactions(self, category):
        return category.transaction_set.exists()

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'order',
            'budget',
            'accumulated',
            'children',
            'has_transactions'
        ]
