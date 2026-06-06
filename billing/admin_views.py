from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsAdminRole, IsApprovedUser
from .models import Invoice, Item
from .serializers import InvoiceSerializer, ItemSerializer


class AdminItemListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsApprovedUser, IsAdminRole]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'hsn_sac_code']
    ordering_fields = ['name', 'price', 'created_at']


class AdminInvoiceListView(generics.ListAPIView):
    queryset = Invoice.objects.all().prefetch_related('items')
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, IsApprovedUser, IsAdminRole]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    ordering_fields = ['invoice_date', 'created_at']
