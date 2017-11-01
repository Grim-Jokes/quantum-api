from django.db.models import Sum

from rest_framework import serializers
from apps.transactions.models import Transaction, Category


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ChildCategorySerializer(serializers.ModelSerializer):
    children = CategorySerializer(many=True)
    value = serializers.SerializerMethodField()

    def get_value(self, instance):
        result = (
            instance.transaction_set.values('category')
            .annotate(total=Sum('value'))
        )

        print(result.query)

        return result

    class Meta:
        model = Category
        fields = ['id', 'name', 'children', 'value']


class SubCategorySerializer(serializers.ModelSerializer):
    children = ChildCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'children']
