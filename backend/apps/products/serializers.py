from rest_framework import serializers
from .models import Product, ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'order']


class ProductSerializer(serializers.ModelSerializer):
    effective_price = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()
    category_name = serializers.CharField(source='category.name', read_only=True, default=None)
    category_order = serializers.IntegerField(source='category.order', read_only=True, default=0)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'type', 'category', 'category_name', 'category_order',
                  'price', 'discount_price', 'effective_price', 'discount_percentage', 'image', 'is_available',
                  'in_stock', 'stock_quantity', 'is_featured', 'order']


class ProductCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ['name', 'description', 'type', 'category', 'price', 'discount_price',
                  'image', 'is_available', 'in_stock', 'stock_quantity', 'is_featured', 'order']
