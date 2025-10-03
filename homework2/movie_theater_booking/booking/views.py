from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.utils import timezone
from .models import Movie, Seat, Booking
from .serializers import (
    MovieSerializer, 
    MovieDetailSerializer,
    SeatSerializer, 
    SeatAvailabilitySerializer,
    BookingSerializer, 
    BookingCreateSerializer
)


class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on movies.
    
    Endpoints:
    - GET /api/movies/ - List all movies
    - POST /api/movies/ - Create a new movie
    - GET /api/movies/{id}/ - Retrieve a movie
    - PUT /api/movies/{id}/ - Update a movie
    - PATCH /api/movies/{id}/ - Partial update
    - DELETE /api/movies/{id}/ - Delete a movie
    - GET /api/movies/{id}/available_seats/ - Get available seats for a movie
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        """Use detailed serializer for retrieve action"""
        if self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieSerializer
    
    @action(detail=True, methods=['get'])
    def available_seats(self, request, pk=None):
        """
        Get all available seats for a specific movie
        GET /api/movies/{id}/available_seats/
        """
        movie = self.get_object()
        booked_seats = Booking.objects.filter(movie=movie).values_list('seat_id', flat=True)
        available_seats = Seat.objects.exclude(id__in=booked_seats)
        
        # Pass movie_id in context for the serializer
        serializer = SeatAvailabilitySerializer(
            available_seats, 
            many=True,
            context={'movie_id': movie.id}
        )
        return Response(serializer.data)


class SeatViewSet(viewsets.ModelViewSet):
    """
    ViewSet for seat availability and booking status.
    
    Endpoints:
    - GET /api/seats/ - List all seats
    - POST /api/seats/ - Create a new seat
    - GET /api/seats/{id}/ - Retrieve a seat
    - PUT /api/seats/{id}/ - Update a seat
    - PATCH /api/seats/{id}/ - Partial update
    - DELETE /api/seats/{id}/ - Delete a seat
    - GET /api/seats/available/ - Get available seats (optionally filtered by movie)
    - GET /api/seats/{id}/check_availability/ - Check if seat is available for a movie
    """
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Get all available seats, optionally filtered by movie
        GET /api/seats/available/?movie_id={id}
        """
        movie_id = request.query_params.get('movie_id', None)
        
        if movie_id:
            # Get seats not booked for a specific movie
            booked_seats = Booking.objects.filter(movie_id=movie_id).values_list('seat_id', flat=True)
            available_seats = Seat.objects.exclude(id__in=booked_seats)
            serializer = SeatAvailabilitySerializer(
                available_seats,
                many=True,
                context={'movie_id': movie_id}
            )
        else:
            # Get all seats that are not marked as booked
            available_seats = Seat.objects.filter(is_booked=False)
            serializer = self.get_serializer(available_seats, many=True)
        
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def check_availability(self, request, pk=None):
        """
        Check if a specific seat is available for a movie
        GET /api/seats/{id}/check_availability/?movie_id={id}
        """
        seat = self.get_object()
        movie_id = request.query_params.get('movie_id')
        
        if not movie_id:
            return Response(
                {"error": "movie_id parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        is_available = not Booking.objects.filter(
            movie_id=movie_id, 
            seat=seat
        ).exists()
        
        return Response({
            "seat_id": seat.id,
            "seat_number": seat.seat_number,
            "movie_id": movie_id,
            "is_available": is_available
        })


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for users to book seats and view their booking history.
    
    Endpoints:
    - GET /api/bookings/ - List user's bookings (or all if staff)
    - POST /api/bookings/ - Create a new booking
    - GET /api/bookings/{id}/ - Retrieve a booking
    - DELETE /api/bookings/{id}/ - Cancel a booking
    - GET /api/bookings/my_bookings/ - Get current user's bookings
    - GET /api/bookings/upcoming/ - Get current user's upcoming bookings
    """
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer
    
    def get_queryset(self):
        """
        Filter bookings to show only the current user's bookings
        unless user is staff
        """
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):
        """Create a new booking"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        
        # Return with the full BookingSerializer for response
        response_serializer = BookingSerializer(booking)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        """
        Cancel a booking (only if it's the user's own booking or user is staff)
        """
        booking = self.get_object()
        if booking.user != request.user and not request.user.is_staff:
            return Response(
                {"error": "You can only cancel your own bookings"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        """
        Get current user's booking history
        GET /api/bookings/my_bookings/
        """
        bookings = Booking.objects.filter(user=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """
        Get current user's upcoming bookings (movies with future release dates)
        GET /api/bookings/upcoming/
        """
        bookings = Booking.objects.filter(
            user=request.user,
            movie__release_date__gte=timezone.now().date()
        )
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)