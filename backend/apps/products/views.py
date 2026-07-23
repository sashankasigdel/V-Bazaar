from rest_framework import generics, permissions
from apps.businesses.models import Business
from .models import Product
from .serializers import ProductSerializer, ProductCreateSerializer


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
        serializer.save(business=business)


class MyProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateSerializer
        return ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(business__owner=self.request.user)
