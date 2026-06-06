from django.contrib import admin
from .models import Invoice, InvoiceItem, Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'hsn_sac_code', 'taxable', 'price', 'user', 'created_at')
    search_fields = ('name', 'hsn_sac_code', 'user__username')
    list_filter = ('type', 'taxable')


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0
    readonly_fields = ('total',)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_email', 'customer_phone', 'invoice_date', 'user', 'created_at')
    search_fields = ('customer_name', 'customer_email', 'customer_phone', 'user__username')
    list_filter = ('invoice_date',)
    inlines = [InvoiceItemInline]
