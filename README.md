Secure Booking System (Django)
Project Description

This project is a Secure Booking System developed using the Django web framework as part of the Secure Software Development (SSD) course. The system allows users to securely register, authenticate, and create booking requests, while administrators manage bookings and monitor system activities through the Django Admin panel.

The application is designed with a strong focus on secure coding practices, OWASP Top 10 mitigation, and accountability through audit logging.

Features

User registration and authentication

Secure login and session management

Booking creation and booking history

Role-Based Access Control (RBAC) using Django Admin

Administrative booking management

Audit logging of user and admin actions

Custom error handling pages (400, 403, 404, 500)

Security Features

This system implements multiple security controls aligned with OWASP Top 10 and OWASP ASVS, including:

Django built-in authentication and password hashing

Role-Based Access Control (RBAC) via Django groups and permissions

Server-side input validation using Django Forms

SQL injection prevention using Django ORM

CSRF protection enabled by default

Secure session management

Custom error pages to prevent information disclosure

Audit logging of authentication and administrative actions

Static security analysis using Bandit

Installation Steps
1. Clone the Repository
git clone https://github.com/WendyDarl/booking_system.git
cd booking_system

2. Create a Virtual Environment
python -m venv venv


Activate the virtual environment:

Windows

venv\Scripts\activate


Linux / macOS

source venv/bin/activate

3. Install Dependencies
pip install django


(Additional dependencies can be added as required.)

How to Run the Application
1. Apply Database Migrations
python manage.py migrate

2. Create Superuser (Admin)
python manage.py createsuperuser

3. Run the Development Server
python manage.py runserver

4. Access the Application

User Interface:
http://127.0.0.1:8000/

Admin Panel:
http://127.0.0.1:8000/admin/

Dependencies

Python 3.x

Django

Bandit (for static security analysis)

Screenshots

Screenshots of the user interface, booking features, Django Admin panel, and audit logs are included in the project report and appendices as part of the SSD assignment submission.

Security Testing

Static Analysis: Bandit

Dynamic Testing: OWASP ZAP

Manual Review: Authentication, access control, input validation, logging

Security testing results are documented in the project report.

Author

GitHub Username: WendyDarl

Course: Secure Software Development

License

This project is developed for academic purposes only.
