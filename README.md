# Django URL-to-QR Code Generator 🔗

This is a simple web application built with Django that allows users to quickly generate and download a custom QR code for any URL.

Users enter a title and a URL, and the application generates a unique QR code image that links directly to that URL, ready for download.

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
3.  The user fills in the **title and URL** and submits the form.
4.  The `generate_qr_code` view receives the `POST` request and validates the form data.
5.  If valid, the view calls the `create_qr_code` helper function (`utils.py`).
6.  This utility function uses the `qrcode` library to generate an image and saves it to the `/media` directory with a unique filename (e.g., **`my_title_a1b2c3d4_qr.png`**).
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
```
QR-CODE-DJANGO/
├── django_qr/             # Main Django project configuration folder
│   ├── __init__.py
│   ├── asgi.py            # ASGI config for async servers
│   ├── settings.py        # Project settings (Database, Static, Media)
│   ├── urls.py            # Main URL routing file
│   ├── forms.py           # Contains the QRCodeForm
│   ├── utils.py           # Helper function to create the QR image
│   ├── views.py           # Contains the core view (generate_qr_code)
│   └── wsgi.py            # WSGI config for (gunicorn)
│
├── media/                 # (Gitignored) Where generated QR codes are saved
│
├── static/                # Static files (CSS, JS, images)
│   └── css/
│       └── style.css      # Custom application styles
│
├── templates/             # HTML templates
│   ├── base.html          # Base template with Bootstrap & dark mode
│   ├── generate_qr_code.html # Home page with the input form
│   └── qr_result.html     # Result page with QR image and download
│
├── venv/                  # (Gitignored) Python virtual environment
├── .gitignore             # Tells Git which files to ignore
├── db.sqlite3             # Development database file
├── manage.py              # Django's command-line utility
├── Procfile               # Declares 'gunicorn' process for deployment
├── requirements.txt       # Python package dependencies
└── runtime.txt            # Specifies Python version for deployment
```
