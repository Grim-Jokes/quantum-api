from django.db.models import Prefetch, Count, Sum

from rest_framework import viewsets, mixins, response
from apps.transactions.models import Transaction, Category, DescriptionInfo
from . import serializers
from scipy import stats
import numpy as np


class Suggestions(mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    def retrieve(self, request, *args, **kwargs):

        trans = Transaction.objects.get(**kwargs)

        desc_info = DescriptionInfo.objects.filter(description=trans.name)

        d = desc_info.filter(min__lte=trans.value, max__gte=trans.value)

        x = stats.stats.array([
            float(trans.value)
        ],
            dtype='float'
        )

        y = stats.stats.array([
            float(d.first().max)
        ],
            dtype='float'
        )

        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        cats = Category.objects.count()

        trans = (
            Transaction.objects
            .filter(
                name=trans.name
            )
            .exclude(category_id=None)
            .values_list('category_id')
            .annotate(count=Count('id'))
        )

        result = dict(trans)
        for key, value in result.items():
            result[key] = {
                'weight': result[key],
                'prob':  result[key] / (cats + result[key] - 1) * 100
            }

        result['total_categories'] = cats

        return response.Response(result)


class TransactionViewSet(
    mixins.UpdateModelMixin,
    viewsets.ReadOnlyModelViewSet
):
    serializer_class = serializers.TransactionSerializer

    def get_queryset(self):

        return (
            Transaction.objects.all()
            .select_related('name')
            .prefetch_related('name__description_info')
            .order_by('id')
        )


class CategoryTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.TransactionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context['count'] = self.get_queryset().count()

        return context

    def get_queryset(self):

        category_pk = self.kwargs['category_pk']

        return Transaction.objects.filter(category_id=category_pk)


class CategoryViewSet(
        mixins.UpdateModelMixin,
        viewsets.ReadOnlyModelViewSet


):

    lookup_value_regex = '\d+'

    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        if self.action in ['retrieve', 'partial_update', 'update']:
            return Category.objects.all().select_related('parent_category')

        p = Prefetch('children', Category.objects.all().order_by('order'))

        res = (
            Category.objects.filter()
            .prefetch_related('transaction_set')
            .prefetch_related(p)
            .prefetch_related('descriptioninfo_set')
            .order_by('order', 'parent_category')
        )

        return res
