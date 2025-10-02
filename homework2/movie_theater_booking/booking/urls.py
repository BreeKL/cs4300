from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, SeatViewSet, BookingViewSet
from . import template_views
from django.contrib import admin
from django.contrib.auth import views as auth_views

# API Router
router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='api-movie')
router.register(r'seats', SeatViewSet, basename='api-seat')
router.register(r'bookings', BookingViewSet, basename='api-booking')

urlpatterns = [
    # Template-based views (HTML pages)
    path('', template_views.movie_list, name='movie_list'),
    path('movie/<int:pk>/', template_views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/book/', template_views.seat_booking, name='seat_booking'),
    path('movie/<int:movie_id>/confirmation/', template_views.booking_confirmation, name='booking_confirmation'),
    path('bookings/', template_views.all_bookings, name='all_bookings'),
    path('booking/<int:booking_id>/cancel/', template_views.cancel_booking, name='cancel_booking'),
    
    # API endpoints (REST API)
    path('api/', include(router.urls)),


]