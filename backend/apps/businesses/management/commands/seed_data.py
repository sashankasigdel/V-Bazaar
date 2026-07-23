from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.businesses.models import BusinessCategory, Business, BusinessHours
from apps.products.models import Product
from apps.reviews.models import Review
from decimal import Decimal
from datetime import time
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding...')
        self.seed_categories()
        self.seed_users()
        self.seed_businesses()
        self.stdout.write(self.style.SUCCESS('Done! Database seeded.'))

    def seed_categories(self):
        cats = [
            ('Restaurants', 'restaurants', '🍽️', 0),
            ('Cafes & Bakeries', 'cafes', '☕', 1),
            ('Grocery', 'grocery', '🛒', 2),
            ('Clothing', 'clothing', '👗', 3),
            ('Electronics', 'electronics', '📱', 4),
            ('Salons & Beauty', 'salons', '💇', 5),
            ('Pharmacies', 'pharmacies', '💊', 6),
            ('Hotels', 'hotels', '🏨', 7),
            ('Repair Shops', 'repair', '🔧', 8),
            ('Education', 'education', '📚', 9),
            ('Hospitals', 'hospitals', '🏥', 10),
            ('Sports & Fitness', 'sports', '🏋️', 11),
        ]
        for name, slug, icon, order in cats:
            BusinessCategory.objects.get_or_create(slug=slug, defaults={'name': name, 'icon': icon, 'order': order})
        self.stdout.write('  Categories created')

    def seed_users(self):
        # Admin
        if not User.objects.filter(email='admin@bazaar.com').exists():
            User.objects.create_superuser(
                username='admin', email='admin@bazaar.com',
                password='admin1234', first_name='Admin', last_name='Bazaar', role='admin'
            )

        # Business owners
        owners = [
            ('owner1@bazaar.com', 'Ramesh', 'Sharma', 'owner1'),
            ('owner2@bazaar.com', 'Sita', 'Thapa', 'owner2'),
            ('owner3@bazaar.com', 'Binod', 'KC', 'owner3'),
        ]
        self.owners = []
        for email, fn, ln, uname in owners:
            u, created = User.objects.get_or_create(email=email, defaults={
                'username': uname, 'first_name': fn, 'last_name': ln,
                'role': 'business_owner', 'is_verified': True, 'phone': '9800000000'
            })
            if created:
                u.set_password('password123')
                u.save()
            self.owners.append(u)

        # Customers
        customers = [
            ('customer1@bazaar.com', 'Aarav', 'Poudel', 'cust1'),
            ('customer2@bazaar.com', 'Priya', 'Gurung', 'cust2'),
        ]
        self.customers = []
        for email, fn, ln, uname in customers:
            u, created = User.objects.get_or_create(email=email, defaults={
                'username': uname, 'first_name': fn, 'last_name': ln,
                'role': 'customer', 'is_verified': True
            })
            if created:
                u.set_password('password123')
                u.save()
            # Create customer profile
            from apps.accounts.models import CustomerProfile
            CustomerProfile.objects.get_or_create(user=u)
            self.customers.append(u)

        self.stdout.write('  Users created')

    def seed_businesses(self):
        rest = BusinessCategory.objects.get(slug='restaurants')
        cafe = BusinessCategory.objects.get(slug='cafes')
        grocery = BusinessCategory.objects.get(slug='grocery')

        data = [
            {
                'owner': self.owners[0], 'category': rest,
                'name': 'Himalayan Spice Kitchen', 'slug': 'himalayan-spice-kitchen',
                'description': 'Authentic Nepali and Indian cuisine in the heart of Pokhara. We use fresh local ingredients and traditional recipes passed down for generations.',
                'short_description': 'Authentic Nepali & Indian cuisine with fresh local ingredients.',
                'address': 'Lakeside Road, Ward 6', 'city': 'Pokhara', 'state': 'Gandaki Pradesh',
                'latitude': Decimal('28.2096'), 'longitude': Decimal('83.9580'),
                'phone': '9856012345', 'whatsapp': '9856012345', 'email': 'himalayan@spice.com',
                'status': 'active', 'is_featured': True,
                'products': [
                    ('Dal Bhat Set', 'Traditional Nepali set meal', '220.00'),
                    ('Chicken Momo (10 pcs)', 'Steamed dumplings with chutney', '180.00'),
                    ('Veg Fried Rice', 'Wok-tossed rice with vegetables', '160.00'),
                    ('Thukpa', 'Tibetan noodle soup', '200.00'),
                    ('Masala Tea', 'Freshly brewed spiced tea', '60.00'),
                ],
            },
            {
                'owner': self.owners[1], 'category': cafe,
                'name': 'Lakeside Coffee House', 'slug': 'lakeside-coffee-house',
                'description': 'A cozy coffee house overlooking Phewa Lake. We source our beans from local Nepali farms and roast them fresh every week.',
                'short_description': 'Specialty coffee & pastries with a stunning lake view.',
                'address': 'Phewa Lake Road, Baidam', 'city': 'Pokhara', 'state': 'Gandaki Pradesh',
                'latitude': Decimal('28.2139'), 'longitude': Decimal('83.9567'),
                'phone': '9867023456', 'whatsapp': '9867023456', 'email': 'lakeside@coffee.com',
                'status': 'active', 'is_featured': True,
                'products': [
                    ('Espresso', 'Single origin Nepali espresso', '120.00'),
                    ('Cappuccino', 'Espresso with steamed milk foam', '180.00'),
                    ('Cold Brew', '12-hour cold brewed coffee', '200.00'),
                    ('Croissant', 'Freshly baked buttery croissant', '150.00'),
                    ('Cheesecake Slice', 'New York style cheesecake', '250.00'),
                ],
            },
            {
                'owner': self.owners[2], 'category': grocery,
                'name': 'Fresh Mart Grocery', 'slug': 'fresh-mart-grocery',
                'description': 'Your neighborhood grocery store with fresh produce, dairy, and household essentials. We source vegetables directly from local farmers every morning.',
                'short_description': 'Fresh produce & groceries sourced daily from local farmers.',
                'address': 'New Road, Ward 9', 'city': 'Pokhara', 'state': 'Gandaki Pradesh',
                'latitude': Decimal('28.2076'), 'longitude': Decimal('83.9856'),
                'phone': '9812034567', 'whatsapp': '9812034567', 'email': 'freshmart@grocery.com',
                'status': 'active', 'is_featured': False,
                'products': [
                    ('Fresh Milk (1L)', 'Farm fresh pasteurized milk', '95.00'),
                    ('Eggs (12 pcs)', 'Free-range farm eggs', '200.00'),
                    ('Basmati Rice (1kg)', 'Premium long grain rice', '180.00'),
                    ('Cooking Oil (1L)', 'Refined sunflower oil', '210.00'),
                    ('Tomatoes (500g)', 'Fresh local tomatoes', '40.00'),
                ],
            },
        ]

        for bdata in data:
            products = bdata.pop('products')
            b, created = Business.objects.get_or_create(slug=bdata['slug'], defaults=bdata)
            if created:
                # Create hours Mon-Sat 8am-9pm, Sun 9am-6pm
                for day in range(6):
                    BusinessHours.objects.get_or_create(business=b, day=day, defaults={
                        'is_closed': False, 'open_time': time(8, 0), 'close_time': time(21, 0)
                    })
                BusinessHours.objects.get_or_create(business=b, day=6, defaults={
                    'is_closed': False, 'open_time': time(9, 0), 'close_time': time(18, 0)
                })
                # Products
                for pname, pdesc, pprice in products:
                    Product.objects.create(
                        business=b, name=pname, description=pdesc,
                        price=pprice, is_available=True, in_stock=True
                    )
                # Reviews
                for customer in self.customers:
                    Review.objects.get_or_create(
                        customer=customer, business=b,
                        defaults={
                            'rating': random.randint(4, 5),
                            'title': 'Great place!',
                            'content': 'Really enjoyed my experience here. Highly recommended!',
                            'is_approved': True,
                        }
                    )
                b.update_rating()
        self.stdout.write('  Businesses, products and reviews created')
