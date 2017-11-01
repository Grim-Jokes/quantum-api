from rest_framework import routers
from rest_framework_nested import routers
from apps.api.v1.transactions import views
from django.conf.urls import include

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet, base_name='categories')

category_router = routers.NestedSimpleRouter(router, r'categories', lookup='category')
category_router.register(r'transactions', views.CategoryTransactionViewSet, base_name='category_transactions')

urlpatterns = router.urls
urlpatterns += category_router.urls
