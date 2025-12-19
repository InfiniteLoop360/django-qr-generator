# Secure Data Transmission System (SDTS) - Defense Grade

> **Status:** Prototype / Deployed
> **Security Level:** AES-128 Encryption + HMAC-SHA256 Integrity Check
> **Classification:** CONFIDENTIAL // NOFORN

## 🛡️ Project Overview
The **Secure Data Transmission System (SDTS)** is a specialized secure communication tool designed for **defense and intelligence operations**. Unlike standard QR code generators, this system prioritizes the **CIA Triad** (Confidentiality, Integrity, Availability) to ensure sensitive data cannot be intercepted, read, or tampered with during transmission.

This tool allows officers to encrypt mission-critical intelligence into a QR code, which can only be decrypted by authorized personnel possessing the specific decryption key. It includes military-grade tamper detection to prevent "Man-in-the-Middle" attacks.

<img width="1557" height="913" alt="Screenshot 2025-12-15 113221" src="https://github.com/user-attachments/assets/04652d55-3e64-4974-9341-ca7b1623913c" />

<img width="1570" height="909" alt="Screenshot 2025-12-15 113239" src="https://github.com/user-attachments/assets/536e583d-a14e-425f-b1d2-f47f76c4dde8" />

<img width="1522" height="912" alt="Screenshot 2025-12-15 114928" src="https://github.com/user-attachments/assets/94e8bc4e-8156-4eff-a118-02b205d1731f" />

<img width="1362" height="908" alt="Screenshot 2025-12-15 114956" src="https://github.com/user-attachments/assets/495f983a-ad46-4b78-9dca-06b01886a126" />

<img width="1400" height="909" alt="Screenshot 2025-12-15 115019" src="https://github.com/user-attachments/assets/c276eec0-2808-4dde-b340-352e83a7454d" />

<img width="1386" height="870" alt="Screenshot 2025-12-15 121541" src="https://github.com/user-attachments/assets/89aaf654-07ba-4da2-9696-29c22502a7f7" />

<img width="1375" height="896" alt="Screenshot 2025-12-15 121552" src="https://github.com/user-attachments/assets/c329aaa1-cbf7-4478-ba15-4fee995d4354" />

<img width="1256" height="905" alt="Screenshot 2025-12-15 121632" src="https://github.com/user-attachments/assets/6af7bdf1-286d-44c5-8a7c-127cfe1b7e6a" />


## 🚀 Key Features

### 1. Military-Grade Confidentiality (AES-128)
* Uses **AES-128 (Fernet)** symmetric encryption to lock raw data.
* Data is completely unreadable (ciphertext) to any standard QR scanner.
* **Key Derivation:** Uses **PBKDF2** (Password-Based Key Derivation Function 2) with 100,000 iterations to derive cryptographically strong keys from user passwords.

### 2. Tamper-Proofing (HMAC Integrity Check)
* Implements **HMAC-SHA256** digital signatures.
* Before encryption, the system generates a cryptographic "fingerprint" of the message.
* **Defense Mechanism:** If an enemy modifies the QR code image or the ciphertext string by even **one byte**, the system detects the signature mismatch and immediately rejects the decryption with a **SECURITY ALERT**.

### 3. Classified Reporting
* Auto-generates professional **"TOP SECRET" PDF Mission Reports**.
* Includes timestamps, unique Mission IDs, and official watermarks for physical dispatch.

### 4. Accountability & Forensics
* **Audit Logging:** Every encryption and decryption attempt is logged in a secure `security_audit.log` file.
* Tracks **IP Addresses**, **Timestamps**, and **Status** (Success/Failure/Tampering) for post-mission analysis.

### 5. Offline-Ready Tactical UI
* The interface is built with **embedded CSS**, ensuring the tool looks modern and functions perfectly even in **air-gapped environments** (no internet connection).

---

## 🛠️ Technology Stack

* **Framework:** Django 5.0 (Python)
* **Cryptography:** `cryptography` (Fernet, HAZMAT primitives)
* **Computer Vision:** `opencv-python` (For reading QR codes from uploaded images)
* **Document Generation:** `reportlab` (For PDF Report generation)
* **QR Processing:** `qrcode[pil]`, `numpy`
* **Frontend:** HTML5, CSS3 (Custom Dark/Light Mode, Offline-Ready)

---

## ⚙️ Installation & Setup

### Prerequisites
* Python 3.10 or higher
* pip (Python Package Installer)

### Step 1: Clone the Repository
```bash
git clone [https://github.com/yourusername/secure-qr-system.git](https://github.com/yourusername/secure-qr-system.git)
cd secure-qr-system
```
### Step 2: Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```
### Step 3: Install Dependencies
```bash
pip install django cryptography qrcode[pil] opencv-python-headless numpy reportlab whitenoise
```
### Step 4: Run Database Migrations
```bash
python manage.py migrate
```
### Step 5: Start the Server
```bash
python manage.py runserver
```
Access the application at: http://127.0.0.1:8000/

## 📖 Usage Guide


### Phase 1: Encryption (The Sender)

1.  Navigate to the Generate page.
2.  Enter the Mission Title (e.g., Operation Alpha) and Confidential Data.
3.  Set a strong Encryption Key (Password).
4.  Click Generate Secure QR.
5.  Output: You can download the raw QR image or the Classified PDF Report.

### Phase 2: Decryption (The Receiver)
1.  Navigate to the Decrypt page.
2.  Upload the QR code image OR Paste the ciphertext string.
3.  Enter the shared Encryption Key.
4.  Click Unlock Data.
5.  Output: You can download the raw QR image or the Classified PDF Report.
    * Success: The original message is displayed.
    * Failure: "Decryption Failed: Incorrect Password."
    * Alert: "SECURITY ALERT: Integrity Check Failed!" (If data was tampered with).
## 📁 Project Structure
```
secure-qr-system/
├── django_qr/
│   ├── forms.py          # Input validation forms
│   ├── utils.py          # CORE LOGIC: Encryption, HMAC, PDF Gen, Logging
│   ├── views.py          # Handles requests and connects UI to Logic
│   ├── urls.py           # Routing
│   └── settings.py       # Configuration
├── media/                # Stores generated QRs and PDFs
├── templates/            # HTML Interface
│   ├── base.html         # Main layout with Offline CSS
│   ├── generate_qr.html  # Encryption Interface
│   ├── decrypt.html      # Decryption Interface
│   └── qr_result.html    # Success Page
├── security_audit.log    # (Created automatically) Logs all actions
└── manage.py
```

---

## ⚠️ Security Note (Prototype)
Salt Management: This prototype uses a static salt for key derivation to ensure portability for demonstration purposes. In a production environment, a unique, random salt would be generated per user and stored in a secure database to prevent rainbow table attacks.

Key Management: The system relies on the user remembering the password. Keys are not stored on the server; if the password is lost, the data is unrecoverable.
---
## 📜 License
This project is developed for educational and demonstration purposes, specifically targeting Defense Technology applications.
