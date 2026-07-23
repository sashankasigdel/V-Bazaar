from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.businesses.models import Business

User = get_user_model()


class Review(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    is_approved = models.BooleanField(default=True)
    owner_reply = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'
        unique_together = ['customer', 'business']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer.email} - {self.business.name} ({self.rating})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.business.update_rating()
