import os
import qrcode
import uuid
from django.conf import settings


def create_qr_code(url, restaurant_name):
    """
    Generate a QR code image for a restaurant URL.
    Adds a unique UUID to prevent file overwriting.
    """
    file_name = f"{restaurant_name.replace(' ', '_').lower()}_{uuid.uuid4().hex[:8]}_menu.png"
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    qr = qrcode.make(url)
    qr.save(file_path)

    return file_name
