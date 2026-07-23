from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    effective_price = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'type', 'price', 'discount_price',
                  'effective_price', 'discount_percentage', 'image', 'is_available',
                  'in_stock', 'stock_quantity', 'is_featured', 'order']


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'type', 'price', 'discount_price',
                  'image', 'is_available', 'in_stock', 'stock_quantity', 'is_featured', 'order']
