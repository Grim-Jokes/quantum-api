from rest_framework import viewsets, mixins, response

from django_filters.rest_framework import (
    DjangoFilterBackend, FilterSet, DateFilter
)

from apps.transactions.models import Transaction

from .. import serializers


class TransactionDateRange(FilterSet):
    start_date = DateFilter(name='date', lookup_expr="gte")
    end_date = DateFilter(name='date', lookup_expr="lte")

    class Meta:
        model = Transaction
        fields = ['date']


class TransactionViewSet(
    mixins.UpdateModelMixin,
    viewsets.ReadOnlyModelViewSet
):
    serializer_class = serializers.TransactionSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = TransactionDateRange
    filter_fields = ('date', )

    def get_queryset(self):

        cat_pk = self.kwargs.get('category_pk')

        if cat_pk:
            trans = Transaction.objects.filter(category_id = cat_pk)
        else:
            trans = Transaction.objects.all()


        result = (trans
            .select_related('name')
            .prefetch_related('name__description_info')
            .order_by('-date')
        )

        limit = self.request.query_params.get('limit')

        if limit:
            limit = int(limit)
            result = result[:limit]

        return result
