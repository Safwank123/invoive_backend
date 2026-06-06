from django.urls import path
from billing.admin_views import AdminInvoiceListView, AdminItemListView
from .views import AdminUserApproveView, AdminUserDeleteView, AdminUserListView

urlpatterns = [
    path('users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('users/<int:pk>/approve/', AdminUserApproveView.as_view(), name='admin-user-approve'),
    path('users/<int:pk>/', AdminUserDeleteView.as_view(), name='admin-user-delete'),
    path('invoices/', AdminInvoiceListView.as_view(), name='admin-invoice-list'),
    path('items/', AdminItemListView.as_view(), name='admin-item-list'),
]
