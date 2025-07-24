# Farmart Backend API

This repository contains the backend server for **Farmart**, a robust e-commerce platform connecting farmers directly with buyers. Built with Django and Django REST Framework, it provides a secure, scalable, and feature-rich API to power the Farmart frontend application.

---

## Key Features

- **User Authentication**: Secure user registration and login using JSON Web Tokens (JWT).
- **Dual User Roles**: Distinct **BUYER** and **FARMER** roles with role-based permissions.
- **Product Management**: Farmers can create, update, and delete livestock listings.
- **Order Management**: Buyers can place orders and track them from creation to payment.
- **Stock Control**: Automatic stock decrementing and sold-out marking.
- **Image Uploads**: Farmers can upload images for their animal listings.
- **M-Pesa Integration**: Seamless payment via Safaricom M-Pesa STK Push.

---

## 🛠️ Technologies Used

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: Djoser, Simple JWT
- **Payments**: Safaricom M-Pesa API
- **Deployment**: Gunicorn, Whitenoise, Render
- **Environment Configuration**: python-decouple

---

## 🚀 Setup and Local Installation

### 1. Prerequisites

- Python 3.8+
- pip
- PostgreSQL

---

### 2. Clone the Repository

```bash
git clone <your-repository-url>
cd farmart_backend
```

### 3. Set Up Virtual Environment

### Create virtual environment
- ** python -m venv venv

### Activate it

### On Mac/Linux:
- ** source venv/bin/activate

### On Windows:
- ** .\venv\Scripts\activate

### 4. Install Dependencies

- ** pip install -r requirements.txt

### 5. Configure Environment Variables

- ** Create a .env file in the root directory with the following content:

### SECURITY
- ** DJANGO_SECRET_KEY='your-strong-secret-key-here'
- ** DEBUG=True

### HOSTS
- ** ALLOWED_HOSTS=localhost,127.0.0.1
- ** BACKEND_DOMAIN=http://127.0.0.1:8000

### DATABASE
- ** DB_NAME='farmart_db'
- ** DB_USER='farmart_user'
- ** DB_PASSWORD='your_db_password'
- ** DB_HOST='localhost'
- ** DB_PORT='5432'
- ** DATABASE_URL='postgres://farmart_user:your_db_password@localhost:5432/farmart_db'

### CORS
- ** CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

### M-PESA
MPESA_ENVIRONMENT=sandbox
MPESA_CONSUMER_KEY=your_mpesa_consumer_key
MPESA_CONSUMER_SECRET=your_mpesa_consumer_secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your_mpesa_passkey

### 6. Run Migrations 

python manage.py makemigrations
python manage.py migrate

### 7. Create a Superuser

python manage.py createsuperuser

### 8. Run the Server 

python manage.py runserver

The API will be available at: http://127.0.0.1:8000/

### M-Pesa Integration Setup

To get the M-Pesa payment functionality working, you need to get credentials from the Safaricom Daraja Developer Portal.

Go to the Safaricom Developer Portal: https://developer.safaricom.co.ke/

1 . Sign Up / Log In: Create a free account or log in.

2 . Create a New App:

3 . Go to the "My Apps" section.

4 . Click "Add a new app".

5 . Give your app a name (e.g., "Farmart").

Make sure to check the box for "Lipa Na M-PESA Sandbox".

6 . Click "Create App".

7 . Get Your Credentials:

8 . Click on your newly created app to view its details.

You will see the Consumer Key and Consumer Secret.

9 . Update Your .env file:

10 . Copy the Consumer Key and paste it as the value for MPESA_CONSUMER_KEY.

11 . Copy the Consumer Secret and paste it as the value for MPESA_CONSUMER_SECRET.

12 . Find Your Passkey and Shortcode:

13 . On the developer portal, navigate to "APIs" -> "Lipa Na M-PESA Online Payment".

14 . Click on "Go to Test Cases" or a similar button.

Here you will find the test credentials, including the Shortcode (usually 174379 for the sandbox) and the Passkey.

15 . Update the MPESA_SHORTCODE and MPESA_PASSKEY values in your .env file.

After filling in all these values in your .env file and restarting your Django server, the M-Pesa STK push will work correctly.
























