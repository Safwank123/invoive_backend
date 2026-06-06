from rest_framework.routers import SimpleRouter
from .views import InvoiceViewSet, ItemViewSet

router = SimpleRouter()
router.register('items', ItemViewSet, basename='items')
router.register('invoices', InvoiceViewSet, basename='invoices')

urlpatterns = router.urls
