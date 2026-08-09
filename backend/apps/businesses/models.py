from django.db import models
from django.contrib.auth import get_user_model
import math

User = get_user_model()


class BusinessCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'business_categories'
        ordering = ['order', 'name']
        verbose_name_plural = 'Business Categories'

    def __str__(self):
        return self.name


class Business(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        PENDING = 'pending', 'Pending'
        SUSPENDED = 'suspended', 'Suspended'

    class TriState(models.TextChoices):
        YES = 'yes', 'Yes'
        NO = 'no', 'No'
        NA = 'na', 'Not Applicable'

    class PaymentMode(models.TextChoices):
        CASH_ONLY = 'cash_only', 'Cash Only'
        ONLINE = 'online', 'Online Payment'

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='businesses')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='branches')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(BusinessCategory, on_delete=models.SET_NULL, null=True, related_name='businesses')
    description = models.TextField(blank=True, default='')
    short_description = models.CharField(max_length=300, blank=True)
    logo = models.ImageField(upload_to='businesses/logos/', blank=True, null=True)
    banner = models.ImageField(upload_to='businesses/banners/', blank=True, null=True)
    address = models.TextField(blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    is_featured = models.BooleanField(default=False)
    payment_mode = models.CharField(max_length=10, choices=PaymentMode.choices, default=PaymentMode.CASH_ONLY)
    card_payment = models.CharField(max_length=3, choices=TriState.choices, default=TriState.NA)
    free_wifi = models.CharField(max_length=3, choices=TriState.choices, default=TriState.NA)
    smoking = models.CharField(max_length=3, choices=TriState.choices, default=TriState.NA)
    offer_package = models.CharField(max_length=3, choices=TriState.choices, default=TriState.NA)
    is_registered = models.BooleanField(null=True, blank=True, default=None)
    has_parking = models.BooleanField(null=True, blank=True, default=None)
    offer_delivery = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)  # Premium badge, admin-only
    accepts_orders = models.BooleanField(default=False)  # Premium: "Accepts Online Orders", admin-only
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_reviews = models.IntegerField(default=0)
    total_orders = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'businesses'
        ordering = ['-is_featured', '-average_rating']

    def __str__(self):
        return self.name

    def distance_from(self, lat, lon):
        if self.latitude is None or self.longitude is None:
            return None
        R = 6371
        lat1, lon1 = float(self.latitude), float(self.longitude)
        lat2, lon2 = float(lat), float(lon)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        return round(R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)), 2)

    def update_rating(self):
        from apps.reviews.models import Review
        from django.db.models import Avg
        reviews = Review.objects.filter(business=self, is_approved=True)
        if reviews.exists():
            avg = reviews.aggregate(Avg('rating'))['rating__avg']
            self.average_rating = round(avg, 2)
            self.total_reviews = reviews.count()
        else:
            self.average_rating = 0
            self.total_reviews = 0
        self.save(update_fields=['average_rating', 'total_reviews'])


class BusinessHours(models.Model):
    DAYS = [(0,'Monday'),(1,'Tuesday'),(2,'Wednesday'),(3,'Thursday'),(4,'Friday'),(5,'Saturday'),(6,'Sunday')]
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='hours')
    day = models.IntegerField(choices=DAYS)
    is_closed = models.BooleanField(default=False)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)

    class Meta:
        db_table = 'business_hours'
        unique_together = ['business', 'day']
        ordering = ['day']

    def __str__(self):
        return f"{self.business.name} - {self.get_day_display()}"


class BusinessGallery(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='businesses/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'business_gallery'
        ordering = ['order']


class Advertisement(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='advertisements')
    image = models.ImageField(upload_to='advertisements/', blank=True, null=True)  # unused going forward — the business's own banner is shown instead
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'advertisements'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"Ad for {self.business.name}"
