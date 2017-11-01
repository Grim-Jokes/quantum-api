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

    class Meta:
        model = Category
        fields = ['id', 'name', 'children']

class SubCategorySerializer(serializers.ModelSerializer):
    children = ChildCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'children']
