import io
from openpyxl import Workbook

EXPORT_COLUMNS = [
    ('business_code', lambda b: b.business_code or ''),
    ('branch_code', lambda b: b.branch_code or ''),
    ('name', lambda b: b.name),
    ('slug', lambda b: b.slug),
    ('category', lambda b: b.category.name if b.category_id else ''),
    ('status', lambda b: b.status),
    ('parent_business', lambda b: b.parent.name if b.parent_id else ''),
    ('owner_email', lambda b: b.owner.email),
    ('phone', lambda b: b.phone),
    ('whatsapp', lambda b: b.whatsapp),
    ('email', lambda b: b.email),
    ('website', lambda b: b.website),
    ('city', lambda b: b.city),
    ('address', lambda b: b.address),
    ('latitude', lambda b: float(b.latitude) if b.latitude is not None else ''),
    ('longitude', lambda b: float(b.longitude) if b.longitude is not None else ''),
    ('average_rating', lambda b: float(b.average_rating)),
    ('total_reviews', lambda b: b.total_reviews),
    ('total_orders', lambda b: b.total_orders),
    ('total_views', lambda b: b.total_views),
    ('is_featured', lambda b: b.is_featured),
    ('is_verified', lambda b: b.is_verified),
    ('accepts_orders', lambda b: b.accepts_orders),
    ('created_at', lambda b: b.created_at.strftime('%Y-%m-%d %H:%M')),
]


def businesses_to_excel(queryset):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Businesses'
    ws.append([col for col, _ in EXPORT_COLUMNS])
    for b in queryset.select_related('category', 'parent', 'owner'):
        ws.append([fn(b) for _, fn in EXPORT_COLUMNS])
    for col_cells in ws.columns:
        length = max(len(str(c.value)) if c.value is not None else 0 for c in col_cells)
        ws.column_dimensions[col_cells[0].column_letter].width = min(max(length + 2, 10), 40)
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf
