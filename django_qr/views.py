from django.shortcuts import render
from django.contrib import messages  # ✅ added for success messages
from .utils import create_qr_code  # ✅ new import
from .forms import QRCodeForm
import qrcode
import os
from django.conf import settings


def generate_qr_code(request):
    if request.method == 'POST':
        form = QRCodeForm(request.POST)
        if form.is_valid():
            res_name = form.cleaned_data['restaurant_name']
            url = form.cleaned_data['url']

            # ✅ Using helper function (cleaner code)
            file_name = create_qr_code(url, res_name)
            qr_url = '/media/' + file_name

            # ✅ Add a success message
            messages.success(request, "QR Code generated successfully!")

            context = {
                'res_name': res_name,
                'qr_url': qr_url,
                'file_name': file_name,
            }
            return render(request, 'qr_result.html', context)
    else:
        form = QRCodeForm()

    return render(request, 'generate_qr_code.html', {'form': form})