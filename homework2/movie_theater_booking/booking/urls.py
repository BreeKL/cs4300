from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, SeatViewSet, BookingViewSet
from . import template_views

# API Router for REST endpoints
router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='api-movie')
router.register(r'seats', SeatViewSet, basename='api-seat')
router.register(r'bookings', BookingViewSet, basename='api-booking')

urlpatterns = [
    # =========================
    # Template-based views (HTML pages)
    # =========================
    path('', template_views.movie_list, name='movie_list'),
    path('movie/<int:pk>/', template_views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/book/', template_views.seat_booking, name='seat_booking'),
    path('movie/<int:movie_id>/confirmation/', template_views.booking_confirmation, name='booking_confirmation'),
    path('bookings/', template_views.all_bookings, name='all_bookings'),
    path('booking/<int:booking_id>/cancel/', template_views.cancel_booking, name='cancel_booking'),
    
    # =========================
    # API endpoints (REST API)
    # =========================
    # All API routes are prefixed with /api/
    path('api/', include(router.urls)),
]

"""
API Endpoints Summary:
======================

MOVIES:
-------
GET    /api/movies/                          - List all movies
POST   /api/movies/                          - Create a new movie (requires auth)
GET    /api/movies/{id}/                     - Retrieve a specific movie
PUT    /api/movies/{id}/                     - Update a movie (requires auth)
PATCH  /api/movies/{id}/                     - Partial update a movie (requires auth)
DELETE /api/movies/{id}/                     - Delete a movie (requires auth)
GET    /api/movies/{id}/available_seats/     - Get available seats for a movie

SEATS:
------
GET    /api/seats/                           - List all seats
POST   /api/seats/                           - Create a new seat (requires auth)
GET    /api/seats/{id}/                      - Retrieve a specific seat
PUT    /api/seats/{id}/                      - Update a seat (requires auth)
PATCH  /api/seats/{id}/                      - Partial update a seat (requires auth)
DELETE /api/seats/{id}/                      - Delete a seat (requires auth)
GET    /api/seats/available/                 - Get available seats
GET    /api/seats/available/?movie_id={id}   - Get available seats for a movie
GET    /api/seats/{id}/check_availability/?movie_id={id} - Check seat availability

BOOKINGS:
---------
GET    /api/bookings/                        - List user's bookings (requires auth)
POST   /api/bookings/                        - Create a new booking (requires auth)
GET    /api/bookings/{id}/                   - Retrieve a specific booking (requires auth)
DELETE /api/bookings/{id}/                   - Cancel a booking (requires auth)
GET    /api/bookings/my_bookings/            - Get current user's bookings (requires auth)
GET    /api/bookings/upcoming/               - Get current user's upcoming bookings (requires auth)

TEMPLATE VIEWS:
--------------
GET    /                                     - Movie list page
GET    /movie/{id}/                          - Movie detail page
GET    /movie/{id}/book/                     - Seat booking page
POST   /movie/{id}/book/                     - Create booking(s)
GET    /movie/{id}/confirmation/             - Booking confirmation page
GET    /bookings/                            - All bookings page
POST   /booking/{id}/cancel/                 - Cancel a booking
"""