from rest_framework import serializers
from .models import Business, BusinessCategory, BusinessHours, BusinessGallery, Advertisement
from datetime import datetime


class BusinessCategorySerializer(serializers.ModelSerializer):
    business_count = serializers.SerializerMethodField()

    class Meta:
        model = BusinessCategory
        fields = ['id', 'name', 'slug', 'icon', 'description', 'business_count']

    def get_business_count(self, obj):
        return obj.businesses.filter(status='active').count()


class BusinessHoursSerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source='get_day_display', read_only=True)

    class Meta:
        model = BusinessHours
        fields = ['id', 'day', 'day_name', 'is_closed', 'open_time', 'close_time']


class BusinessGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessGallery
        fields = ['id', 'image', 'caption', 'order']


class BusinessListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    distance = serializers.SerializerMethodField()
    is_open = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Business
        fields = ['id', 'name', 'slug', 'category_name', 'category_icon', 'category_slug', 'logo', 'banner',
                  'short_description', 'address', 'city', 'latitude', 'longitude',
                  'average_rating', 'total_reviews', 'is_featured',
                  'distance', 'is_open', 'is_saved', 'status', 'phone',
                  'accepts_orders', 'is_verified']

    def get_distance(self, obj):
        request = self.context.get('request')
        if request:
            lat = request.query_params.get('lat')
            lon = request.query_params.get('lon')
            if lat and lon:
                try:
                    return obj.distance_from(float(lat), float(lon))
                except Exception:
                    pass
        return None

    def get_is_open(self, obj):
        now = datetime.now()
        day = now.weekday()
        try:
            hours = obj.hours.get(day=day)
            if hours.is_closed:
                return False
            if hours.open_time and hours.close_time:
                return hours.open_time <= now.time() <= hours.close_time
        except Exception:
            pass
        return None

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                return request.user.customer_profile.saved_businesses.filter(id=obj.id).exists()
            except Exception:
                pass
        return False


class BusinessDetailSerializer(serializers.ModelSerializer):
    category = BusinessCategorySerializer(read_only=True)
    hours = BusinessHoursSerializer(many=True, read_only=True)
    gallery = BusinessGallerySerializer(many=True, read_only=True)
    is_open = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Business
        fields = ['id', 'name', 'slug', 'category', 'description', 'short_description',
                  'logo', 'banner', 'address', 'city', 'state', 'latitude', 'longitude',
                  'phone', 'whatsapp', 'email', 'website', 'facebook', 'instagram',
                  'status', 'is_featured', 'accepts_orders', 'is_verified',
                  'payment_mode', 'card_payment', 'free_wifi', 'smoking', 'offer_package',
                  'is_registered', 'has_parking', 'offer_delivery',
                  'average_rating', 'total_reviews', 'total_orders',
                  'hours', 'gallery', 'is_open', 'is_saved', 'distance', 'created_at']

    def get_is_open(self, obj):
        now = datetime.now()
        try:
            hours = obj.hours.get(day=now.weekday())
            if hours.is_closed:
                return False
            if hours.open_time and hours.close_time:
                return hours.open_time <= now.time() <= hours.close_time
        except Exception:
            pass
        return None

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                return request.user.customer_profile.saved_businesses.filter(id=obj.id).exists()
            except Exception:
                pass
        return False

    def get_distance(self, obj):
        request = self.context.get('request')
        if request:
            lat = request.query_params.get('lat')
            lon = request.query_params.get('lon')
            if lat and lon:
                try:
                    return obj.distance_from(float(lat), float(lon))
                except Exception:
                    pass
        return None


def _unique_slug(name):
    from django.utils.text import slugify
    slug = slugify(name)
    base_slug = slug
    i = 1
    while Business.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{i}"
        i += 1
    return slug


class BusinessCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['name', 'category', 'description', 'short_description', 'logo', 'banner',
                  'address', 'city', 'state', 'latitude', 'longitude',
                  'phone', 'whatsapp', 'email', 'website', 'facebook', 'instagram',
                  'payment_mode', 'card_payment', 'free_wifi', 'smoking', 'offer_package',
                  'is_registered', 'has_parking', 'offer_delivery']

    def create(self, validated_data):
        validated_data['slug'] = _unique_slug(validated_data.get('name', ''))
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class AdminBusinessCreateSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = Business
        fields = ['name', 'category', 'description', 'short_description', 'logo', 'banner',
                  'address', 'city', 'state', 'latitude', 'longitude',
                  'phone', 'whatsapp', 'email', 'website', 'facebook', 'instagram',
                  'status', 'is_featured',
                  'payment_mode', 'card_payment', 'free_wifi', 'smoking', 'offer_package',
                  'is_registered', 'has_parking', 'offer_delivery',
                  'is_verified', 'accepts_orders', 'owner_email']

    def create(self, validated_data):
        from apps.accounts.services import get_or_create_dummy_business_owner
        owner_email = validated_data.pop('owner_email', '') or None
        validated_data['slug'] = _unique_slug(validated_data.get('name', ''))
        owner, _created = get_or_create_dummy_business_owner(
            phone=validated_data.get('phone', ''), email=owner_email,
        )
        validated_data['owner'] = owner
        return super().create(validated_data)


class AdvertisementSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='business.name', read_only=True)
    business_slug = serializers.CharField(source='business.slug', read_only=True)

    class Meta:
        model = Advertisement
        fields = ['id', 'image', 'business_name', 'business_slug', 'is_active', 'order']
