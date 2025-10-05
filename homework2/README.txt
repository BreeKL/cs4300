# README for Homework 2 - CS4300 

# CS4300 Homework 2 
# Brianne Leatherman 
# Oct 4, 2025 

================================================================================
PROJECT DESCRIPTION
================================================================================

This is a Movie Theater Booking System built with Django and Django REST Framework.
The application allows users to:
- Browse available movies
- View movie details including duration and release dates
- Book seats for movies through an interactive seat selection interface
- View all bookings in the system
- Cancel bookings
- Access all functionality through both a web interface and REST API

The system prevents double-booking of seats and provides a responsive, 
Bootstrap-based user interface.

================================================================================
TECHNOLOGY STACK
================================================================================

- Python 3.12
- Django 5.2.7
- Django REST Framework
- Bootstrap 5.3.0
- SQLite (development) / PostgreSQL (production)
- Gunicorn (production server)
- WhiteNoise (static file serving)

================================================================================
FILE STRUCTURE
================================================================================

movie_theater_booking/
├── booking/                          # Main Django app
│   ├── migrations/                   # Database migrations
│   ├── templates/booking/            # HTML templates
│   │   ├── base.html                 # Base template with Bootstrap
│   │   ├── movie_list.html           # Movie listing page
│   │   ├── movie_detail.html         # Individual movie details
│   │   ├── seat_booking.html         # Interactive seat booking
│   │   ├── booking_confirmation.html # Booking success page
│   │   └── all_bookings.html         # View all bookings
│   ├── static/booking/               # Static files (CSS, JS)
│   ├── admin.py                      # Django admin configuration
│   ├── models.py                     # Data models (Movie, Seat, Booking)
│   ├── serializers.py                # DRF serializers for API
│   ├── views.py                      # API ViewSets
│   ├── template_views.py             # Template-based views
│   ├── urls.py                       # URL routing
│   └── tests.py                      # Unit and integration tests
├── movie_theater_booking/            # Project settings
│   ├── settings.py                   # Django settings
│   ├── urls.py                       # Root URL configuration
│   ├── wsgi.py                       # WSGI application
│   └── asgi.py                       # ASGI application
├── manage.py                         # Django management script
├── requirements.txt                  # Python dependencies
├── build.sh                          # Render deployment script
├── db.sqlite3                        # SQLite database (development)
└── README.txt                        # This file

================================================================================
SETUP INSTRUCTIONS
================================================================================

1. VIRTUAL ENVIRONMENT SETUP
-----------------------------

# Navigate to root directory
cd ~/cs4300/homework2

# Create virtual environment
python3 -m venv hw2_venv

# Activate virtual environment
# On Linux/Mac:
source hw2_venv/bin/activate

# On Windows:
hw2_venv\Scripts\activate

# You should see (hw2_venv) in your terminal prompt


2. INSTALL DEPENDENCIES
------------------------

# Ensure you are in the root directory
cd ~/cs4300/homework2

# Ensure virtual environment is activated
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Required packages include:
# - Django==5.2.7
# - djangorestframework
# - django-bootstrap5
# - gunicorn
# - whitenoise
# - dj-database-url
# - psycopg2-binary


3. DATABASE SETUP
------------------

# Navigate to project directory
cd ~/cs4300/homework2/movie_theater_booking

# Run migrations to create database tables
python manage.py makemigrations
python manage.py migrate

# Create a superuser for admin access
python manage.py createsuperuser
# Follow prompts to set username, email (optional), and password


4. CREATE TEST DATA (OPTIONAL)
-------------------------------

# Ensure you are in the project directory
cd ~/cs4300/homework2/movie_theater_booking

# Open Django shell
python manage.py shell

# Run the following Python commands:
from booking.models import Movie, Seat
from datetime import date, timedelta

# Create movies
Movie.objects.create(
    title="The Matrix Resurrections",
    description="Return to the world of two realities.",
    release_date=date.today() + timedelta(days=7),
    duration=148
)

Movie.objects.create(
    title="Dune: Part Two",
    description="Paul Atreides unites with Chani and the Fremen.",
    release_date=date.today() + timedelta(days=14),
    duration=166
)

# Create seats (A1-A10, B1-B10, C1-C10, etc.)
for row in ['A', 'B', 'C', 'D', 'E']:
    for num in range(1, 11):
        Seat.objects.create(seat_number=f"{row}{num}")

# Exit shell
exit()

================================================================================
RUNNING THE APPLICATION
================================================================================

DEVELOPMENT SERVER
------------------

# Ensure virtual environment is activated
# Ensure you are in the project directory: homework2/movie_theater_booking
# Start the Django development server

python manage.py runserver 0.0.0.0:3000

# Access the application at: http://localhost:3000/


# Or for default port 8000:
python manage.py runserver

# Access at http://localhost:8000/


PRODUCTION WEBSITE
-----------------------------

Visit the production website at https://cs4300-5imc.onrender.com/

================================================================================
RUNNING TESTS
================================================================================

# Ensure you are in the project directory: homework2/movie_theater_booking
# Run all tests
python manage.py test

# Run with verbose output
python manage.py test --verbosity=2

# Run specific test classes
python manage.py test booking.tests.MovieModelTest
python manage.py test booking.tests.MovieAPITest
python manage.py test booking.tests.SeatAPITest
python manage.py test booking.tests.BookingAPITest
python manage.py test booking.tests.TemplateViewsTest

# Test coverage (46 tests total):
# - 17 Model Unit Tests
# - 23 API Integration Tests  
# - 6 Template View Tests

All tests verify:
- Model creation and validation
- API endpoint responses (200, 201, 204, 400, 403, 404)
- Data format validation
- Authentication and permissions
- Business logic (duplicate booking prevention)
- Template rendering

================================================================================
ACCESSING THE APPLICATION
================================================================================

WEB INTERFACE
-------------

Local server:             http://localhost:3000
Render deployment:        https://cs4300-5imc.onrender.com

Main Pages:
- Home/Movie List:        /
- Movie Detail:           /movie/1/
- Seat Booking:           /movie/1/book/
- All Bookings:           /bookings/
- Django Admin:           /admin/
- Web-browsable API       /api/


REST API ENDPOINTS
------------------

MOVIES:
GET    /api/movies/                          - List all movies
POST   /api/movies/                          - Create a new movie (requires auth)
GET    /api/movies/{id}/                     - Retrieve a specific movie
PUT    /api/movies/{id}/                     - Update a movie (requires auth)
PATCH  /api/movies/{id}/                     - Partial update (requires auth)
DELETE /api/movies/{id}/                     - Delete a movie (requires auth)
GET    /api/movies/{id}/available_seats/     - Get available seats for a movie

SEATS:
GET    /api/seats/                           - List all seats
POST   /api/seats/                           - Create a new seat (requires auth)
GET    /api/seats/{id}/                      - Retrieve a specific seat
PUT    /api/seats/{id}/                      - Update a seat (requires auth)
DELETE /api/seats/{id}/                      - Delete a seat (requires auth)
GET    /api/seats/available/                 - Get available seats
GET    /api/seats/available/?movie_id={id}   - Get available seats for movie
GET    /api/seats/{id}/check_availability/?movie_id={id} - Check availability

BOOKINGS:
GET    /api/bookings/                        - List user's bookings (requires auth)
POST   /api/bookings/                        - Create a booking (requires auth)
GET    /api/bookings/{id}/                   - Retrieve a booking (requires auth)
DELETE /api/bookings/{id}/                   - Cancel a booking (requires auth)
GET    /api/bookings/my_bookings/            - User's booking history (requires auth)
GET    /api/bookings/upcoming/               - User's upcoming bookings (requires auth)


API TESTING WITH CURL
---------------------

# List all movies
curl http://localhost:3000/api/movies/
curl https://cs4300-5imc.onrender.com/api/movies/

# Get specific movie
curl http://localhost:3000/api/movies/1/
curl https://cs4300-5imc.onrender.com/api/movies/1/

# List all seats
curl http://localhost:3000/api/seats/
curl https://cs4300-5imc.onrender.com/api/seats/

# Check available seats for a movie
curl http://localhost:3000/api/seats/available/?movie_id=1
curl https://cs4300-5imc.onrender.com/api/seats/available/?movie_id=1

# Get available seats for a specific movie
curl http://localhost:3000/api/movies/1/available_seats/
curl https://cs4300-5imc.onrender.com/api/movies/1/available_seats

# Authenticated requests require token or session

# Use the browsable API at http://localhost:3000/api/ or 
# https://cs4300-5imc.onrender.com/api/ for easier testing


================================================================================
DEPLOYMENT ON RENDER
================================================================================

The application is configured for deployment on Render.com
Current deployment address: https://cs4300-5imc.onrender.com

Deployment files:
- build.sh: Automated build script
- requirements.txt: Python dependencies
- settings.py: Production-ready configuration with environment variables

Environment Variables for Render:
- SECRET_KEY: Django secret key 
- DEBUG: Set to False for production
- DATABASE_URL: PostgreSQL connection string (auto-provided by Render)
- ALLOWED_HOSTS: Your Render app URL

Deployment Steps:
1. Push code to GitHub
2. Create Web Service on Render
3. Link GitHub repository
4. Add PostgreSQL database
5. Set environment variables
6. Deploy (automatic)
(Migration and superuser creation included in build.sh)


================================================================================
DISCLAIMER OF GENERATIVE AI CONTRIBUTIONS
================================================================================

This project was developed with assistance from OpenAI’s ChatGPT (GPT-5) and
Anthropic's Claude (Sonnet 4.5).
AI contributions include:

- Django models (Movie, Seat, Booking)
- DRF Serializers with validation logic 
- Template-based views for web interface
- HTML templates with Bootstrap styling
- JavaScript for interactive seat selection
- URL routing configuration
- Comprehensive test suite (46 tests)
- REST API endpoint design
- Authentication and permission strategies
- Documentation
- Render deployment scripts

The student was responsible for requirements definition, debugging 
environment-specific issues, and deployment. All final development, testing, 
and submission choices were made by Brianne Leatherman

================================================================================
TROUBLESHOOTING
================================================================================

DATABASE LOCKED ERROR:
- Stop the development server (Ctrl+C)
- Run migrations again
- Restart server

STATIC FILES NOT LOADING:
- Run: python manage.py collectstatic
- Ensure DEBUG=True in development

PORT ALREADY IN USE:
- Kill existing process: lsof -ti:3000 | xargs kill -9
- Or use a different port: python manage.py runserver 0.0.0.0:8001

MIGRATIONS NOT APPLYING:
- Delete db.sqlite3 (development only!)
- Delete booking/migrations/ except __init__.py
- Run: python manage.py makemigrations
- Run: python manage.py migrate

TESTS FAILING:
- Run: python manage.py test --verbosity=2 for details
- Check that all dependencies are installed

IMPORT ERRORS:
- Ensure virtual environment is activated
- Run: pip install -r requirements.txt
- Verify Python version: python --version

================================================================================
ADDITIONAL RESOURCES
================================================================================

Django Documentation: https://docs.djangoproject.com/
DRF Documentation: https://www.django-rest-framework.org/
Bootstrap Documentation: https://getbootstrap.com/docs/5.3/
Render Deployment Guide: https://render.com/docs/deploy-django

================================================================================
LICENSE
================================================================================

This project is created for educational purposes as part of CS4300 coursework.

================================================================================
CONTACT
================================================================================

Student: Brianne Leatherman
Email: bleather@uccs.edu

================================================================================
END OF README
================================================================================
