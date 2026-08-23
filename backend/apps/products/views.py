from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from apps.businesses.models import Business
from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductCreateSerializer, ProductCategorySerializer


def _owned_business_q(user):
    """Matches rows whose business is owned directly by `user`, or is a branch of
    a business `user` owns (Business Admin managing their branches)."""
    return Q(business__owner=user) | Q(business__parent__owner=user)


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
        return Product.objects.filter(_owned_business_q(self.request.user), business__slug=self.kwargs['slug'])

    def perform_create(self, serializer):
        business = Business.objects.filter(Q(owner=self.request.user) | Q(parent__owner=self.request.user)).get(slug=self.kwargs['slug'])
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
        return Product.objects.filter(_owned_business_q(self.request.user))

    def perform_update(self, serializer):
        category = serializer.validated_data.get('category')
        if category and category.business_id != serializer.instance.business_id:
            raise ValidationError({'category': 'Category does not belong to this business.'})
        serializer.save()


class MyProductCategoryListView(generics.ListCreateAPIView):
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProductCategory.objects.filter(_owned_business_q(self.request.user), business__slug=self.kwargs['slug'])

    def perform_create(self, serializer):
        business = Business.objects.filter(Q(owner=self.request.user) | Q(parent__owner=self.request.user)).get(slug=self.kwargs['slug'])
        serializer.save(business=business)


class MyProductCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProductCategory.objects.filter(_owned_business_q(self.request.user))
