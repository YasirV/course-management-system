Django Course Registration System

A simple course registration system built with Django and PostgreSQL.

Features:

Faculty members can offer courses

Students can register for up to 2 courses

User authentication and role-based access control

PostgreSQL database integration


Installation

Clone the repository:

git clone https://github.com/your-username/django-course-registration.git

cd django-course-registration


Create a virtual environment and activate it:

python -m venv venv

source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Configure PostgreSQL:

Create a PostgreSQL database named course_registration_db

Update the database settings in settings.py with your database credentials


Apply migrations:

python manage.py makemigrations

python manage.py migrate


Run the development server:

python manage.py runserver


Access the application at http://127.0.0.1:8000


Project Structure:

accounts - User authentication and profile management

courses - Course and registration management


How to Use:

Register as either a Student or Faculty member

For Faculty:

Log in and offer courses through the faculty dashboard

Manage your offered courses


For Students:

Log in and view available courses

Register for up to 2 courses

View and manage your course registrations
