import re
from rest_framework import serializers
from .models import Invoice, InvoiceItem, Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'type', 'hsn_sac_code', 'taxable', 'price', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        item_type = attrs.get('type', getattr(self.instance, 'type', None))
        code = attrs.get('hsn_sac_code', getattr(self.instance, 'hsn_sac_code', None))

        if item_type in [Item.Type.GOODS, Item.Type.SERVICE]:
            if not code:
                raise serializers.ValidationError('HSN/SAC code is required for goods and services.')
            if not re.fullmatch(r'\d{6}', code):
                raise serializers.ValidationError('HSN/SAC must be exactly 6 digits.')

        return attrs


class InvoiceItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)

    class Meta:
        model = InvoiceItem
        fields = ['id', 'item', 'item_name', 'quantity', 'unit_price', 'total']
        read_only_fields = ['id', 'item_name', 'total']


class InvoiceItemCreateSerializer(serializers.Serializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    quantity = serializers.IntegerField(min_value=1)
    unit_price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)

    def validate_item(self, value):
        request = self.context.get('request')
        if request and value.user != request.user:
            raise serializers.ValidationError('Item must belong to the authenticated user.')
        return value

    def validate(self, attrs):
        attrs['unit_price'] = attrs.get('unit_price', attrs['item'].price)
        return attrs


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id',
            'customer_name',
            'customer_email',
            'customer_phone',
            'customer_address',
            'invoice_date',
            'created_at',
            'items',
        ]
        read_only_fields = ['id', 'created_at', 'items']


class InvoiceCreateSerializer(serializers.ModelSerializer):
    items = InvoiceItemCreateSerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            'customer_name',
            'customer_email',
            'customer_phone',
            'customer_address',
            'invoice_date',
            'items',
        ]

    def validate_customer_phone(self, value):
        if not re.fullmatch(r'^\+?\d{10,15}$', value):
            raise serializers.ValidationError('Enter a valid customer phone number with 10 to 15 digits.')
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(user=self.context['request'].user, **validated_data)
        for item_data in items_data:
            InvoiceItem.objects.create(
                invoice=invoice,
                item=item_data['item'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
            )
        return invoice
