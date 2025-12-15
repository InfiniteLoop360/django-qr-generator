import os
import uuid
import qrcode
import base64
import cv2
import numpy as np
import datetime
import hmac
import hashlib
from django.conf import settings

# Security Imports
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# PDF Imports
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors


# --- 1. SECURITY HELPER: Derive TWO Keys ---
def get_keys_from_password(password):
    """
    Derives TWO separate keys from the single password:
    1. Encryption Key (AES) - To lock the data.
    2. Integrity Key (HMAC) - To sign the data (tamper proofing).
    """
    salt = b'indian_army_internship_demo_salt'

    # Generate 64 bytes (32 for encryption + 32 for HMAC)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=64,
        salt=salt,
        iterations=100000,
    )
    derived_material = kdf.derive(password.encode())

    # Split into two keys
    enc_key = base64.urlsafe_b64encode(derived_material[:32])
    hmac_key = derived_material[32:]
    return enc_key, hmac_key


# --- 2. AUDIT LOGGING ---
def log_security_event(action, status, ip_address, details=""):
    """
    Logs every access attempt to a secure audit file.
    """
    log_file = os.path.join(settings.BASE_DIR, 'security_audit.log')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] | IP: {ip_address} | ACTION: {action} | STATUS: {status} | {details}\n"

    with open(log_file, "a") as f:
        f.write(entry)


# --- 3. PDF GENERATOR ---
def generate_pdf_report(qr_file_path, title, mission_id):
    pdf_name = f"Mission_Report_{mission_id}.pdf"
    pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_name)

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # --- STEP 1: DRAW WATERMARK (CORRECTED MATH) ---
    c.saveState()
    c.setFont("Helvetica-Bold", 90)  # Made it slightly bigger
    c.setFillColorRGB(0.92, 0.92, 0.92)  # Very light grey (Subtle)

    # The Fix: Move to center -> Rotate -> Draw at (0,0)
    c.translate(width / 2, height / 2)
    c.rotate(45)
    c.drawCentredString(0, 0, "CONFIDENTIAL")
    c.restoreState()

    # --- STEP 2: DRAW HEADER ---
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.darkred)
    c.drawCentredString(width / 2, height - 50, "TOP SECRET")

    # --- STEP 3: DRAW MISSION DETAILS ---
    c.setFont("Courier-Bold", 14)
    c.setFillColor(colors.black)

    c.drawString(50, height - 120, f"OPERATION: {title.upper()}")
    c.drawString(50, height - 140, f"MISSION ID: {mission_id}")
    c.drawString(50, height - 160, f"TIMESTAMP: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # --- STEP 4: DRAW QR CODE ---
    # Draw border
    c.setLineWidth(2)
    c.rect(width / 2 - 105, height / 2 - 55, 210, 210)
    # Draw image
    c.drawImage(qr_file_path, width / 2 - 100, height / 2 - 50, width=200, height=200)

    # --- STEP 5: DRAW FOOTER ---
    c.setFont("Courier-Bold", 12)
    c.setFillColor(colors.darkred)
    c.drawCentredString(width / 2, 200, "WARNING: ENCRYPTED INTELLIGENCE")

    c.setFont("Courier", 10)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, 180,
                        "Unauthorized decryption is a punishable offense under the Official Secrets Act.")

    c.save()
    return pdf_name


# --- 4. CORE LOGIC: Encrypt + Sign ---
def create_secure_assets(data, title, password, ip_address):
    # A. Derive Keys
    enc_key, hmac_key = get_keys_from_password(password)

    # B. Encrypt Data (AES)
    f = Fernet(enc_key)
    encrypted_bytes = f.encrypt(data.encode())

    # C. Sign Data (HMAC) - Create a "Fingerprint"
    # We sign the encrypted bytes to ensure nobody changed them
    signature = hmac.new(hmac_key, encrypted_bytes, hashlib.sha256).hexdigest()

    # D. Combine: format is "SIGNATURE:ENCRYPTED_MESSAGE"
    final_payload = f"{signature}:{encrypted_bytes.decode('utf-8')}"

    # E. Generate QR
    mission_id = uuid.uuid4().hex[:8]
    qr_filename = f"{title.replace(' ', '_').lower()}_{mission_id}_secure.png"
    qr_path = os.path.join(settings.MEDIA_ROOT, qr_filename)

    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(final_payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(qr_path)

    # F. Generate PDF
    pdf_filename = generate_pdf_report(qr_path, title, mission_id)

    # G. Log It
    log_security_event("ENCRYPTION", "SUCCESS", ip_address, f"Created Mission: {title}")

    return qr_filename, pdf_filename


# --- 5. CORE LOGIC: Verify + Decrypt ---
def read_qr_from_image(image_file):
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    return data


def decrypt_data(payload, password, ip_address):
    try:
        # A. Split the payload into Signature and Ciphertext
        if ":" not in payload:
            log_security_event("DECRYPTION", "FAILED", ip_address, "Invalid Data Format")
            return None, "Error: Data format invalid. Not a secure QR."

        submitted_signature, encrypted_data_str = payload.split(":", 1)
        encrypted_bytes = encrypted_data_str.encode('utf-8')

        # B. Derive Keys again
        enc_key, hmac_key = get_keys_from_password(password)

        # C. Verify HMAC (Check for Tampering)
        expected_signature = hmac.new(hmac_key, encrypted_bytes, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(submitted_signature, expected_signature):
            # CRITICAL ALERT: Data was tampered with!
            log_security_event("DECRYPTION", "ALERT", ip_address, "TAMPERING DETECTED")
            return None, "SECURITY ALERT: Integrity Check Failed! Data has been modified."

        # D. Decrypt (AES)
        f = Fernet(enc_key)
        decrypted_msg = f.decrypt(encrypted_bytes).decode('utf-8')

        log_security_event("DECRYPTION", "SUCCESS", ip_address, "Data Accessed")
        return decrypted_msg, None

    except Exception as e:
        log_security_event("DECRYPTION", "FAILED", ip_address, "Wrong Password")
        return None, "Decryption Failed: Incorrect Password."