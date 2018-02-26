from rest_framework_nested import routers
from .transactions import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet, base_name='categories')

router.register(
    r'transactions',
    views.TransactionViewSet,
    base_name='transactions'
)

router.register(
    r'^(?P<type>((income)|(expense)))',
    views.FilteredCategories,
    base_name="category_types"
)

category_router = routers.NestedSimpleRouter(
    router,
    r'categories',
    lookup='category_types'
)

category_router.register(
    r'transactions',
    views.TransactionViewSet,
    base_name='category_transactions'
)

urlpatterns = router.urls
urlpatterns += category_router.urls
