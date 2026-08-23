from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from .models import Business, BusinessCategory, BusinessHours, BusinessGallery, Advertisement
from .serializers import (
    BusinessListSerializer, BusinessDetailSerializer,
    BusinessCreateUpdateSerializer, BusinessCategorySerializer,
    BusinessHoursSerializer, BusinessGallerySerializer, AdvertisementSerializer
)
import math


class BusinessCategoryListView(generics.ListAPIView):
    serializer_class = BusinessCategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return BusinessCategory.objects.annotate(
            active_business_count=Count('businesses', filter=Q(businesses__status='active'))
        ).order_by('-active_business_count', 'name')


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


def _owned_businesses(user):
    """A Business Admin (owner of a parent business) manages that business AND all
    of its branches, even branches reassigned to a different Branch Admin login.
    A Branch Admin manages only the branch(es) they directly own.
    """
    return Business.objects.filter(Q(owner=user) | Q(parent__owner=user)).distinct()


class MyBusinessListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BusinessCreateUpdateSerializer
        return BusinessListSerializer

    def get_queryset(self):
        return _owned_businesses(self.request.user)


class MyBusinessDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BusinessCreateUpdateSerializer
        return BusinessDetailSerializer

    def get_queryset(self):
        return _owned_businesses(self.request.user)


class BusinessHoursView(generics.ListCreateAPIView):
    serializer_class = BusinessHoursSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BusinessHours.objects.filter(business__in=_owned_businesses(self.request.user), business__slug=self.kwargs['slug'])

    def perform_create(self, serializer):
        business = _owned_businesses(self.request.user).get(slug=self.kwargs['slug'])
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
        return BusinessGallery.objects.filter(business__in=_owned_businesses(self.request.user), business__slug=self.kwargs['slug'])

    def perform_create(self, serializer):
        business = _owned_businesses(self.request.user).get(slug=self.kwargs['slug'])
        serializer.save(business=business)


class BusinessGalleryDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BusinessGallery.objects.filter(business__in=_owned_businesses(self.request.user))


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_businesses(request):
    businesses = Business.objects.filter(status='active', is_featured=True)[:8]
    serializer = BusinessListSerializer(businesses, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def active_advertisements(request):
    ads = Advertisement.objects.filter(
        is_active=True, business__status='active',
    ).exclude(business__banner='').exclude(business__banner__isnull=True).select_related('business')[:5]
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
        business = _owned_businesses(request.user).get(slug=slug)
        return Response({
            'total_views': business.total_views,
            'total_orders': business.total_orders,
            'average_rating': str(business.average_rating),
            'total_reviews': business.total_reviews,
        })
    except Business.DoesNotExist:
        return Response({'error': 'Not found.'}, status=404)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def archive_branch(request, slug):
    """Business Admin archives one of their own branches. Only the parent business's
    owner may do this — not the branch's own (possibly reassigned) Branch Admin,
    and not for a top-level business (only Super Admin archives those)."""
    try:
        business = Business.objects.get(slug=slug, parent__owner=request.user)
    except Business.DoesNotExist:
        return Response({'error': 'Branch not found or you do not manage it.'}, status=404)
    business.status = Business.Status.ARCHIVED
    business.save(update_fields=['status'])
    return Response({'slug': business.slug, 'status': business.status})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def restore_branch(request, slug):
    try:
        business = Business.objects.get(slug=slug, parent__owner=request.user)
    except Business.DoesNotExist:
        return Response({'error': 'Branch not found or you do not manage it.'}, status=404)
    business.status = Business.Status.ACTIVE
    business.save(update_fields=['status'])
    return Response({'slug': business.slug, 'status': business.status})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reset_branch_admin_password(request, slug):
    """Business Admin resets the password of the Branch Admin assigned to one of
    their branches. Returns the new password once — it is never stored or shown again."""
    import secrets
    try:
        business = Business.objects.get(slug=slug, parent__owner=request.user)
    except Business.DoesNotExist:
        return Response({'error': 'Branch not found or you do not manage it.'}, status=404)
    new_password = secrets.token_urlsafe(9)
    business.owner.set_password(new_password)
    business.owner.save(update_fields=['password'])
    return Response({'owner_email': business.owner.email, 'owner_phone': business.owner.phone, 'new_password': new_password})
