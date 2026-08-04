from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Business, BusinessCategory, BusinessHours, BusinessGallery, Advertisement
from .serializers import (
    BusinessListSerializer, BusinessDetailSerializer,
    BusinessCreateUpdateSerializer, BusinessCategorySerializer,
    BusinessHoursSerializer, BusinessGallerySerializer, AdvertisementSerializer
)
import math


class BusinessCategoryListView(generics.ListAPIView):
    queryset = BusinessCategory.objects.all()
    serializer_class = BusinessCategorySerializer
    permission_classes = [permissions.AllowAny]


class BusinessListView(generics.ListAPIView):
    serializer_class = BusinessListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'city', 'category__name']
    ordering_fields = ['average_rating', 'total_orders', 'created_at']

    def get_queryset(self):
        qs = Business.objects.filter(status='active').select_related('category')
        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')
        radius = self.request.query_params.get('radius', 10)
        category = self.request.query_params.get('category')
        min_rating = self.request.query_params.get('min_rating')
        city = self.request.query_params.get('city')

        if category:
            qs = qs.filter(category__slug=category)
        if min_rating:
            qs = qs.filter(average_rating__gte=min_rating)
        if city:
            qs = qs.filter(city__icontains=city)

        if lat and lon:
            try:
                lat, lon, radius = float(lat), float(lon), float(radius)
                delta_lat = radius / 111.0
                delta_lon = radius / (111.0 * math.cos(math.radians(lat)))
                qs = qs.filter(
                    latitude__range=(lat - delta_lat, lat + delta_lat),
                    longitude__range=(lon - delta_lon, lon + delta_lon)
                )
            except ValueError:
                pass

        open_now = self.request.query_params.get('open_now')
        if open_now == 'true':
            from datetime import datetime
            now = datetime.now()
            qs = qs.filter(
                hours__day=now.weekday(),
                hours__is_closed=False,
                hours__open_time__lte=now.time(),
                hours__close_time__gte=now.time()
            )
        return qs


class BusinessDetailView(generics.RetrieveAPIView):
    queryset = Business.objects.filter(status='active')
    serializer_class = BusinessDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.total_views += 1
        instance.save(update_fields=['total_views'])
        return Response(self.get_serializer(instance).data)


class MyBusinessListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BusinessCreateUpdateSerializer
        return BusinessListSerializer

    def get_queryset(self):
        return Business.objects.filter(owner=self.request.user)


class MyBusinessDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BusinessCreateUpdateSerializer
        return BusinessDetailSerializer

    def get_queryset(self):
        return Business.objects.filter(owner=self.request.user)


class BusinessHoursView(generics.ListCreateAPIView):
    serializer_class = BusinessHoursSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BusinessHours.objects.filter(business__owner=self.request.user, business__slug=self.kwargs['slug'])

    def perform_create(self, serializer):
        business = Business.objects.get(slug=self.kwargs['slug'], owner=self.request.user)
        # Update or create
        BusinessHours.objects.update_or_create(
            business=business,
            day=serializer.validated_data['day'],
            defaults={
                'is_closed': serializer.validated_data.get('is_closed', False),
                'open_time': serializer.validated_data.get('open_time'),
                'close_time': serializer.validated_data.get('close_time'),
            }
        )


class BusinessGalleryListView(generics.ListCreateAPIView):
    serializer_class = BusinessGallerySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BusinessGallery.objects.filter(business__owner=self.request.user, business__slug=self.kwargs['slug'])

    def perform_create(self, serializer):
        business = Business.objects.get(slug=self.kwargs['slug'], owner=self.request.user)
        serializer.save(business=business)


class BusinessGalleryDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BusinessGallery.objects.filter(business__owner=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_businesses(request):
    businesses = Business.objects.filter(status='active', is_featured=True)[:8]
    serializer = BusinessListSerializer(businesses, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def active_advertisements(request):
    ads = Advertisement.objects.filter(is_active=True, business__status='active').select_related('business')[:5]
    serializer = AdvertisementSerializer(ads, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def nearby_businesses(request):
    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')
    if not lat or not lon:
        return Response({'error': 'lat and lon required.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        lat, lon = float(lat), float(lon)
        radius = float(request.query_params.get('radius', 5))
    except ValueError:
        return Response({'error': 'Invalid coordinates.'}, status=400)
    delta_lat = radius / 111.0
    delta_lon = radius / (111.0 * math.cos(math.radians(lat)))
    businesses = Business.objects.filter(
        status='active',
        latitude__range=(lat - delta_lat, lat + delta_lat),
        longitude__range=(lon - delta_lon, lon + delta_lon),
    )
    business_list = sorted(businesses, key=lambda b: b.distance_from(lat, lon))
    serializer = BusinessListSerializer(business_list, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def business_analytics(request, slug):
    try:
        business = Business.objects.get(slug=slug, owner=request.user)
        return Response({
            'total_views': business.total_views,
            'total_orders': business.total_orders,
            'average_rating': str(business.average_rating),
            'total_reviews': business.total_reviews,
        })
    except Business.DoesNotExist:
        return Response({'error': 'Not found.'}, status=404)
