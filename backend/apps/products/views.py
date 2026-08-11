from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from apps.businesses.models import Business
from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductCreateSerializer, ProductCategorySerializer


class BusinessProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Product.objects.filter(business__slug=self.kwargs['slug'], is_available=True)


class MyProductListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(business__slug=self.kwargs['slug'], business__owner=self.request.user)

    def perform_create(self, serializer):
        business = Business.objects.get(slug=self.kwargs['slug'], owner=self.request.user)
        category = serializer.validated_data.get('category')
        if category and category.business_id != business.id:
            raise ValidationError({'category': 'Category does not belong to this business.'})
        serializer.save(business=business)


class MyProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateSerializer
        return ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(business__owner=self.request.user)

    def perform_update(self, serializer):
        category = serializer.validated_data.get('category')
        if category and category.business_id != serializer.instance.business_id:
            raise ValidationError({'category': 'Category does not belong to this business.'})
        serializer.save()


class MyProductCategoryListView(generics.ListCreateAPIView):
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProductCategory.objects.filter(business__slug=self.kwargs['slug'], business__owner=self.request.user)

    def perform_create(self, serializer):
        business = Business.objects.get(slug=self.kwargs['slug'], owner=self.request.user)
        serializer.save(business=business)


class MyProductCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProductCategory.objects.filter(business__owner=self.request.user)
