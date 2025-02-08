from rest_framework import serializers
from .models import *
from myapp.models import *

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")  # For response

    class Meta:
        model = OrderItem
        fields = ["order_item_id", "order", "product", "product_name", "amount"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["order_id", "user", "items"]