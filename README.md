# DjangoBlog

A travel blog built with Django as a learning project.

## Features
- Post list with pagination
- Create, edit and delete posts (login required)
- Cover image upload
- User registration, login, logout and password reset
- Category filtering
- Custom 403, 404 and 500 error pages

## Setup
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate`
4. Install packages: `pip install -r requirements.txt`
5. Create a `.env` file containing `SECRET_KEY`, `DEBUG=True` and `ALLOWED_HOSTS=127.0.0.1,localhost`
6. Run `python manage.py migrate`
7. Run `python manage.py runserver`

## Screenshots
(Add 2-3 screenshots here)