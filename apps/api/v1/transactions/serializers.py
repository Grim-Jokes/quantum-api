from django.db.models import Sum

from rest_framework import serializers
from apps.transactions.models import Transaction, Category


def get_income(instance):
    return instance.parent_category_id == 1 or instance.parent_category.parent_category_id == 1


def get_limit(instance):
    if not instance.children.exists():
        return instance.limit
    return None


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class GrandChildCategorySerializer(serializers.ModelSerializer):
    values = serializers.SerializerMethodField()
    income = serializers.SerializerMethodField()

    def get_values(self, instance):
        result = (
            instance.transaction_set.aggregate(total=Sum('value'))
        )

        result['limit'] = get_limit(instance)

        return result

    def get_income(self, instance):
        return get_income(instance)

    class Meta:
        model = Category
        fields = ['id', 'name', 'income', 'values']


class ChildCategorySerializer(serializers.ModelSerializer):
    children = GrandChildCategorySerializer(many=True)
    values = serializers.SerializerMethodField()
    income = serializers.SerializerMethodField()

    def get_values(self, instance):
        result = (
            instance.transaction_set.aggregate(total=Sum('value'))
        )

        result['limit'] = get_limit(instance)

        return result

    def get_income(self, instance):
        return get_income(instance)

    class Meta:
        model = Category
        fields = ['id', 'name', 'income', 'values',  'children']


class RootCategorySerializer(serializers.ModelSerializer):
    children = ChildCategorySerializer(many=True)
    income = serializers.SerializerMethodField()

    def get_income(self, instance):
        return instance.id == 1

    class Meta:
        model = Category
        fields = ['id', 'name', 'income', 'children']
