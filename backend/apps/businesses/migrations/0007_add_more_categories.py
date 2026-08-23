from django.db import migrations

# (name, slug, emoji icon, frontend SVG icon key used by CATEGORY_ICON_PATHS in app.js)
NEW_CATEGORIES = [
    ('Bakery', 'bakery', '🍞', 'bakery'),
    ('Bars & Pubs', 'bars-pubs', '🍸', 'bars-pubs'),
    ('Gym & Fitness', 'gym-fitness', '🏋️', 'gym-fitness'),
    ('Banking & Finance', 'banking-finance', '🏦', 'banking-finance'),
    ('Real Estate', 'real-estate', '🏠', 'real-estate'),
    ('Travel Agency', 'travel-agency', '✈️', 'travel-agency'),
    ('Photography', 'photography', '📷', 'photography'),
    ('Laundry & Dry Cleaning', 'laundry', '🧺', 'laundry'),
    ('Furniture', 'furniture', '🛋️', 'furniture'),
    ('Hardware & Tools', 'hardware', '🔨', 'hardware'),
    ('Jewelry', 'jewelry', '💎', 'jewelry'),
    ('Bookstore', 'bookstore', '📚', 'bookstore'),
    ('Pet Store', 'pet-store', '🐾', 'pet-store'),
    ('Florist', 'florist', '💐', 'florist'),
    ('Event Planning', 'event-planning', '🎈', 'event-planning'),
    ('Insurance', 'insurance', '🛡️', 'insurance'),
    ('Legal Services', 'legal-services', '⚖️', 'legal-services'),
    ('Accounting & Tax', 'accounting', '🧮', 'accounting'),
    ('Veterinary', 'veterinary', '🐶', 'veterinary'),
    ('Dental Clinic', 'dental-clinic', '🦷', 'dental-clinic'),
    ('Opticians & Eyewear', 'opticians', '👓', 'opticians'),
    ('Tailors', 'tailors', '🧵', 'tailors'),
    ('Printing & Copy', 'printing-copy', '🖨️', 'printing-copy'),
    ('Car Dealership', 'car-dealership', '🚗', 'car-dealership'),
    ('Gas Station', 'gas-station', '⛽', 'gas-station'),
    ('Taxi & Transport', 'transport-taxi', '🚕', 'transport-taxi'),
    ('Courier & Logistics', 'courier-logistics', '📦', 'courier-logistics'),
    ('Spa & Wellness', 'spa-wellness', '🧖', 'spa-wellness'),
    ('Tattoo & Piercing', 'tattoo-piercing', '🖋️', 'tattoo-piercing'),
    ('Music School', 'music-school', '🎵', 'music-school'),
    ('Art & Craft', 'art-craft', '🎨', 'art-craft'),
    ('Toy Store', 'toy-store', '🧸', 'toy-store'),
    ('Mobile & Telecom', 'mobile-telecom', '📱', 'mobile-telecom'),
    ('Cinema & Entertainment', 'cinema-entertainment', '🎬', 'cinema-entertainment'),
    ('Night Clubs', 'night-clubs', '🪩', 'night-clubs'),
    ('Catering', 'catering', '🍽️', 'catering'),
    ('Agriculture Supplies', 'agriculture', '🌾', 'agriculture'),
    ('Construction & Contractors', 'construction', '👷', 'construction'),
    ('Interior Design', 'interior-design', '🖌️', 'interior-design'),
    ('Cleaning Services', 'cleaning-services', '🧹', 'cleaning-services'),
    ('Security Services', 'security-services', '🔒', 'security-services'),
    ('Daycare & Childcare', 'daycare', '🧸', 'daycare'),
    ('NGO & Non-Profit', 'ngo-nonprofit', '❤️', 'ngo-nonprofit'),
    ('Government Services', 'government-services', '🏛️', 'government-services'),
    ('Religious & Temple', 'religious-temple', '🛕', 'religious-temple'),
    ('Wedding Planners', 'wedding-planners', '💍', 'wedding-planners'),
    ('Driving School', 'driving-school', '🚘', 'driving-school'),
    ('Coaching Centers', 'coaching-centers', '📖', 'coaching-centers'),
    ('Cosmetics & Beauty', 'cosmetics-beauty', '💄', 'cosmetics-beauty'),
    ('Motorcycle & Bike Shop', 'motorcycle-bike', '🏍️', 'motorcycle-bike'),
]


def add_categories(apps, schema_editor):
    BusinessCategory = apps.get_model('businesses', 'BusinessCategory')
    for name, slug, emoji, _icon_key in NEW_CATEGORIES:
        BusinessCategory.objects.update_or_create(
            slug=slug,
            defaults={'name': name, 'icon': emoji},
        )


def remove_categories(apps, schema_editor):
    BusinessCategory = apps.get_model('businesses', 'BusinessCategory')
    slugs = [slug for _name, slug, _emoji, _icon_key in NEW_CATEGORIES]
    BusinessCategory.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0006_advertisement_image_optional'),
    ]

    operations = [
        migrations.RunPython(add_categories, remove_categories),
    ]
