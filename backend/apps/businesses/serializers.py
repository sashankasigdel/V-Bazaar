from rest_framework import serializers
from .models import Business, BusinessCategory, BusinessHours, BusinessGallery
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
    distance = serializers.SerializerMethodField()
    is_open = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Business
        fields = ['id', 'name', 'slug', 'category_name', 'category_icon', 'logo',
                  'short_description', 'address', 'city', 'latitude', 'longitude',
                  'average_rating', 'total_reviews', 'is_featured',
                  'distance', 'is_open', 'is_saved', 'status', 'phone']

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
                  'status', 'is_featured', 'average_rating', 'total_reviews', 'total_orders',
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


class BusinessCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['name', 'category', 'description', 'short_description', 'logo', 'banner',
                  'address', 'city', 'state', 'latitude', 'longitude',
                  'phone', 'whatsapp', 'email', 'website', 'facebook', 'instagram']

    def create(self, validated_data):
        from django.utils.text import slugify
        slug = slugify(validated_data.get('name', ''))
        base_slug = slug
        i = 1
        while Business.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{i}"
            i += 1
        validated_data['slug'] = slug
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
