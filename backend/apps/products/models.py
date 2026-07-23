from django.db import models
from apps.businesses.models import Business


class Product(models.Model):
    class Type(models.TextChoices):
        PRODUCT = 'product', 'Product'
        SERVICE = 'service', 'Service'

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=10, choices=Type.choices, default=Type.PRODUCT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    stock_quantity = models.IntegerField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'products'
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.business.name} - {self.name}"

    @property
    def effective_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def discount_percentage(self):
        if self.discount_price and self.price:
            return round(((self.price - self.discount_price) / self.price) * 100)
        return 0
