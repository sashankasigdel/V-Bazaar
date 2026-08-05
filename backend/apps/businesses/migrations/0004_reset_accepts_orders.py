from django.db import migrations


def reset_accepts_orders(apps, schema_editor):
    Business = apps.get_model('businesses', 'Business')
    Business.objects.update(accepts_orders=False)


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0003_business_flags'),
    ]

    operations = [
        migrations.RunPython(reset_accepts_orders, migrations.RunPython.noop),
    ]
