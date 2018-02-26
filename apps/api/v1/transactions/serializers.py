from django.db.models import Sum

from rest_framework import serializers
from apps.transactions.models import Transaction, Category, DescriptionInfo


class TransactionSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='name.name')

    def update(self, instance, data):
        updated_instance = super().update(instance, data)

        desc_info, created = DescriptionInfo.objects.get_or_create(
            description=updated_instance.name,
            defaults={
                'category': updated_instance.category,
                'min': 0,
                'max': 0
            }
        )
        if desc_info.min == 0:
            desc_info.min = instance.value
        else:
            desc_info.min = min(instance.value, desc_info.min)

        desc_info.max = max(instance.value, desc_info.max)

        desc_info.save()

        return updated_instance

    class Meta:
        model = Transaction
        fields = '__all__'


class DescriptionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="description.name")
    min = serializers.DecimalField(max_digits=8, decimal_places=2)
    max = serializers.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        model = DescriptionInfo
        fields = ['name', 'min', 'max']


class CategorySerializer(serializers.ModelSerializer):

    budget = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source="limit"
    )

    accumulated = serializers.SerializerMethodField()

    def get_accumulated(self, category):
        total = (
            category.transaction_set
            .aggregate(total=Sum('value'))
            .get('total', 0.00)
        )

        return 0.00 if not total else total

    has_transactions = serializers.SerializerMethodField()

    def get_has_transactions(self, category):
        return category.transaction_set.exists()

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'type',
            'order',
            'budget',
            'accumulated',
            'has_transactions'
        ]
