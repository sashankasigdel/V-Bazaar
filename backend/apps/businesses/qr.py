import io
import os
import textwrap

import qrcode
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

FRONTEND_DIR = os.path.join(settings.BASE_DIR.parent, 'frontend')
LOGO_PATH = os.path.join(FRONTEND_DIR, 'images', 'icon-192.png')

CANVAS_W = 640
PADDING = 40
QR_SIZE = 440
SAFFRON = '#EE6C29'


def _font(size):
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def _centered_text(draw, y, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    draw.text(((CANVAS_W - (bbox[2] - bbox[0])) // 2, y), text, font=font, fill=fill)


def business_target_url(business, request):
    return f"{request.scheme}://{request.get_host()}/business/?slug={business.slug}"


def generate_qr_card(business, target_url):
    """Returns a BytesIO PNG: V-Bazaar branding + the business/branch name on top
    of a QR code (with the app logo centered in it) linking to its public page."""
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=2)
    qr.add_data(target_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color='#1a1a1a', back_color='white').convert('RGB')
    qr_img = qr_img.resize((QR_SIZE, QR_SIZE))

    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH).convert('RGBA')
        logo_size = QR_SIZE // 5
        logo = logo.resize((logo_size, logo_size))
        backing_size = logo_size + 16
        backing = Image.new('RGBA', (backing_size, backing_size), 'white')
        backing_pos = ((QR_SIZE - backing_size) // 2, (QR_SIZE - backing_size) // 2)
        qr_img.paste(backing, backing_pos)
        logo_pos = ((QR_SIZE - logo_size) // 2, (QR_SIZE - logo_size) // 2)
        qr_img.paste(logo, logo_pos, logo)

    name = business.name
    code = business.branch_code or business.business_code or ''
    label = 'Branch' if business.parent_id else 'Business'

    title_font = _font(32)
    name_font = _font(24)
    small_font = _font(16)

    wrapped = textwrap.wrap(name, width=26) or ['']
    name_block_h = len(wrapped) * 30

    canvas_h = PADDING + 40 + 24 + QR_SIZE + 24 + name_block_h + 26 + PADDING
    canvas = Image.new('RGB', (CANVAS_W, canvas_h), 'white')
    draw = ImageDraw.Draw(canvas)

    y = PADDING
    _centered_text(draw, y, 'V-Bazaar', title_font, SAFFRON)
    y += 40 + 24

    canvas.paste(qr_img, ((CANVAS_W - QR_SIZE) // 2, y))
    y += QR_SIZE + 24

    for line in wrapped:
        _centered_text(draw, y, line, name_font, '#1a1a1a')
        y += 30

    subtitle = f"{label}{' · ' + code if code else ''}"
    _centered_text(draw, y + 6, subtitle, small_font, '#888888')

    buf = io.BytesIO()
    canvas.save(buf, format='PNG')
    buf.seek(0)
    return buf
