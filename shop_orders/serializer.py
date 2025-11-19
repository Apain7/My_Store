from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product_name', 'product_image', 'price', 'quantity')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'customer_name', 'customer_email', 'customer_phone', 'customer_address', 'notes', 'total_price', 'status', 'created_at', 'items')
        read_only_fields = ('id', 'status', 'created_at')

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        # احسب الإجمالي من العناصر إن لم يرسل total_price صحيح
        total = 0
        for it in items_data:
            total += float(it.get('price', 0)) * int(it.get('quantity', 1))

        validated_data['total_price'] = total
        order = Order.objects.create(**validated_data)
        for it in items_data:
            OrderItem.objects.create(order=order, **it)
        return order
