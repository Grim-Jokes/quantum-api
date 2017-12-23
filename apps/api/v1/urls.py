from rest_framework_nested import routers
from .transactions import views

router = routers.DefaultRouter()
router.register(r'suggestions', views.Suggestions, base_name='suggestions')
router.register(r'categories', views.CategoryViewSet, base_name='categories')
router.register(
    r'transactions',
    views.TransactionViewSet,
    base_name='transactions'
)

category_router = routers.NestedSimpleRouter(
    router,
    r'categories',
    lookup='category'
)
category_router.register(
    r'transactions',
    views.CategoryTransactionViewSet,
    base_name='category_transactions'
)

urlpatterns = router.urls
urlpatterns += category_router.urls
