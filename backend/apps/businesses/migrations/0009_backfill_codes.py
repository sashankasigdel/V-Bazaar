from django.db import migrations


def backfill_codes(apps, schema_editor):
    BusinessCategory = apps.get_model('businesses', 'BusinessCategory')
    Business = apps.get_model('businesses', 'Business')
    CodeSequence = apps.get_model('businesses', 'CodeSequence')

    def next_value(name):
        seq, _ = CodeSequence.objects.get_or_create(name=name)
        seq.last_value += 1
        seq.save(update_fields=['last_value'])
        return seq.last_value

    for cat in BusinessCategory.objects.filter(category_code__isnull=True).order_by('id'):
        cat.category_code = f"CAT{next_value('category'):04d}"
        cat.save(update_fields=['category_code'])

    for biz in Business.objects.filter(parent__isnull=True, business_code__isnull=True).order_by('id'):
        biz.business_code = f"B{next_value('business'):07d}"
        biz.save(update_fields=['business_code'])

    for br in Business.objects.filter(parent__isnull=False, branch_code__isnull=True).order_by('id'):
        br.branch_code = f"BR{next_value('branch'):07d}"
        br.save(update_fields=['branch_code'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0008_unique_codes_and_archive'),
    ]

    operations = [
        migrations.RunPython(backfill_codes, noop),
    ]
