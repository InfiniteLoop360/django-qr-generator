# Django Restaurant Menu QR Code Generator 🍽️

This is a simple web application built with Django that allows restaurants to quickly generate and download a custom QR code for their digital menu.

Users enter their restaurant's name and a URL to their online menu. The application then generates a unique QR code image that links directly to that URL, ready for download.

## 🚀 Live Demo

*(Replace this with your live URL once deployed)*
[https://your-project-name.onrender.com](https://your-project-name.onrender.com)

## 📸 Screenshots

*(Replace these with links to your own screenshots)*

| Form Page | Result Page |
| :---: | :---: |
| ![Screenshot of the QR generator form](https/your-image-host.com/form.png) | ![Screenshot of the QR result page](https/your-image-host.com/result.png) |

## ✨ Features

* **Simple & Clean UI:** An easy-to-use form built with Bootstrap 5.
* **Instant QR Code Generation:** Creates a QR code from any valid URL.
* **Downloadable Image:** Allows users to download the generated QR code as a `.png` file.
* **🎨 Light/Dark Mode:** Includes a theme toggler in the navbar that saves the user's preference in `localStorage`.
* **Smooth Animations:** Features a success checkmark and fade-in animations on the result page for a better user experience.
* **Form Validation:** Ensures a valid URL is entered before attempting to generate a code.
* **Deployment Ready:** Pre-configured with `gunicorn`, `whitenoise`, and a `Procfile` for easy hosting on platforms like Render or Heroku.

## ⚙️ How It Works

1.  A user visits the home page (`/`), which is rendered by the `generate_qr_code` view (`views.py`) using the `generate_qr_code.html` template.
2.  The template displays the `QRCodeForm` (`forms.py`).
3.  The user fills in the restaurant name and menu URL and submits the form.
4.  The `generate_qr_code` view receives the `POST` request and validates the form data.
5.  If valid, the view calls the `create_qr_code` helper function (`utils.py`).
6.  This utility function uses the `qrcode` library to generate an image and saves it to the `/media` directory with a unique filename (e.g., `my_restaurant_a1b2c3d4_menu.png`).
7.  The view then renders the `qr_result.html` template, passing in the URL and filename of the newly created image.
8.  The user sees the success animation and the QR code, with buttons to "Download" or "Generate Another."

## 🛠️ Tech Stack

* **Backend:** Django
* **Frontend:** HTML5, Bootstrap 5, JavaScript (for theme toggle & animations)
* **QR Generation:** `qrcode` (Python library)
* **Deployment:** Gunicorn (WSGI Server), Whitenoise (Static File Serving)
* **Database:** SQLite (default for development)

## 📦 Getting Started (Local Setup)

Follow these instructions to get a copy of the project running on your local machine.

### Prerequisites

* Python 3.10+
* Pip (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/django-qr-code.git](https://github.com/your-username/django-qr-code.git)
    cd django-qr-code
    ```

2.  **Create and activate a virtual environment:**
    * **macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * **Windows:**
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: The `Pillow` library is a dependency of `qrcode` for image generation, which is why it's in `requirements.txt`)*

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

6.  **Open the application:**
    Open your web browser and navigate to `http://127.0.0.1:8000/`.

## ☁️ Deployment Guide (Render)

This project is configured for deployment on Render. The `media` folder (where QR codes are saved) is in `.gitignore`, so you must use a **Persistent Disk** on Render to store user-uploaded files.

1.  Push your code to a GitHub repository.
2.  On Render, create a new **"Web Service"** and connect it to your repository.
3.  Set the following properties:
    * **Runtime:** `Python 3` (Render will use the `runtime.txt` file).
    * **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
    * **Start Command:** `gunicorn django_qr.wsgi`
4.  Go to the **"Disks"** section for your new service.
5.  Click **"Add Disk"** and configure it:
    * **Name:** `media`
    * **Mount Path:** `/app/media` (This *must* match the `MEDIA_ROOT` setting)
    * **Size:** 1 GB (or as needed)
6.  Deploy! Your application will be live, and generated QR codes will be saved to the persistent disk.

## 📁 Project Structure
