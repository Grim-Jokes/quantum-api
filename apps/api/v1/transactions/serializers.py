from rest_framework import serializers
from apps.transactions.models import Transaction, Category

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class ParentCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    parent_category = ParentCategorySerializer()

    class Meta:
        model = Category
        fields = '__all__'
