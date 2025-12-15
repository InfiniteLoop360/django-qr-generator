from django.shortcuts import render
from django.contrib import messages
from .utils import create_secure_assets, decrypt_data, read_qr_from_image
from .forms import QRCodeForm, DecryptForm


# Helper to get IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generate_qr_code(request):
    if request.method == 'POST':
        form = QRCodeForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            data = form.cleaned_data['data']
            password = form.cleaned_data['password']
            ip = get_client_ip(request)

            # Updated function call returns BOTH QR and PDF
            file_name, pdf_name = create_secure_assets(data, title, password, ip)
            qr_url = '/media/' + file_name
            pdf_url = '/media/' + pdf_name

            messages.success(request, "Secure Transmission Assets Generated!")
            return render(request, 'qr_result.html', {
                'title': title,
                'qr_url': qr_url,
                'pdf_url': pdf_url,  # Pass PDF to template
                'file_name': file_name
            })
    else:
        form = QRCodeForm()

    return render(request, 'generate_qr_code.html', {'form': form})


def decrypt_qr_code(request):
    result = None
    error = None
    ip = get_client_ip(request)

    if request.method == 'POST':
        form = DecryptForm(request.POST, request.FILES)
        if form.is_valid():
            password = form.cleaned_data['password']
            encrypted_text = form.cleaned_data['encrypted_data']
            image = form.cleaned_data['qr_image']

            if image and not encrypted_text:
                try:
                    extracted_text = read_qr_from_image(image)
                    if extracted_text:
                        encrypted_text = extracted_text
                    else:
                        error = "No QR code found in the image."
                except Exception:
                    error = "Error processing image file."

            if encrypted_text and not error:
                # Updated function returns (Result, ErrorMessage)
                decrypted_msg, err_msg = decrypt_data(encrypted_text, password, ip)

                if decrypted_msg:
                    result = decrypted_msg
                else:
                    error = err_msg  # Now shows specific error (Tampered vs Wrong Password)
            elif not error:
                error = "Please upload an image or paste text."
    else:
        form = DecryptForm()

    return render(request, 'decrypt.html', {'form': form, 'result': result, 'error': error})