from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsApprovedUser
from .models import Invoice, Item
from .permissions import IsOwnerOrAdmin
from .serializers import InvoiceCreateSerializer, InvoiceSerializer, ItemSerializer


class ItemViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsApprovedUser, IsOwnerOrAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'hsn_sac_code']
    ordering_fields = ['name', 'price', 'created_at']

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InvoiceViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated, IsApprovedUser, IsOwnerOrAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    ordering_fields = ['invoice_date', 'created_at']

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user).prefetch_related('items')

    def get_serializer_class(self):
        if self.action == 'create':
            return InvoiceCreateSerializer
        return InvoiceSerializer

    def perform_create(self, serializer):
        serializer.save()
