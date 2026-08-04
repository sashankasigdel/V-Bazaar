from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.businesses.models import Business

User = get_user_model()

DEMO_EMAILS = [
    'admin@bazaar.com',
    'owner1@bazaar.com',
    'owner2@bazaar.com',
    'owner3@bazaar.com',
    'customer1@bazaar.com',
    'customer2@bazaar.com',
]

DEMO_BUSINESS_SLUGS = [
    'himalayan-spice-kitchen',
    'lakeside-coffee-house',
    'fresh-mart-grocery',
]


class Command(BaseCommand):
    help = 'Remove seeded demo users and demo businesses (safe to re-run)'

    def handle(self, *args, **kwargs):
        biz_count, _ = Business.objects.filter(slug__in=DEMO_BUSINESS_SLUGS).delete()
        self.stdout.write(f'  Removed demo businesses (and related products/reviews/hours): {biz_count} rows')

        users = User.objects.filter(email__in=DEMO_EMAILS)
        user_emails = list(users.values_list('email', flat=True))
        user_count, _ = users.delete()
        self.stdout.write(f'  Removed demo users: {user_emails} ({user_count} rows)')

        self.stdout.write(self.style.SUCCESS('Done! Demo data removed.'))
