from rest_framework import serializers
from .models import Order, OrderItem, OrderStatusHistory


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price', 'subtotal']


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ['status', 'note', 'created_at']


class OrderListSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='business.name', read_only=True)
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'business_name', 'status', 'total', 'payment_method', 'is_paid', 'item_count', 'created_at']

    def get_item_count(self, obj):
        return obj.items.count()


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)
    business_name = serializers.CharField(source='business.name', read_only=True)
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    customer_phone = serializers.CharField(source='customer.phone', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'customer_phone', 'business_name', 'status',
                  'payment_method', 'is_paid', 'delivery_address', 'subtotal',
                  'delivery_fee', 'total', 'notes', 'items', 'status_history', 'created_at']


class OrderCreateSerializer(serializers.Serializer):
    business = serializers.IntegerField()
    items = serializers.ListField(child=serializers.DictField())
    delivery_address = serializers.CharField()
    payment_method = serializers.ChoiceField(choices=Order.PaymentMethod.choices)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        from apps.businesses.models import Business
        business = Business.objects.filter(id=data.get('business')).first()
        if not business:
            raise serializers.ValidationError({'detail': 'Business not found.'})
        if not business.accepts_orders:
            raise serializers.ValidationError({'detail': 'This business is not currently accepting online orders.'})
        return data

    def create(self, validated_data):
        from apps.businesses.models import Business
        from apps.products.models import Product
        items_data = validated_data.pop('items')
        business = Business.objects.get(id=validated_data.pop('business'))
        order = Order.objects.create(
            customer=self.context['request'].user,
            business=business,
            **validated_data
        )
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                unit_price=product.effective_price,
            )
        order.calculate_totals()
        OrderStatusHistory.objects.create(order=order, status=order.status)
        # Update business order count
        business.total_orders += 1
        business.save(update_fields=['total_orders'])
        return order
