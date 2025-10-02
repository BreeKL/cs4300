from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.utils import timezone
from .models import Movie, Seat, Booking


class MovieViewSet(viewsets.ViewSet):
    """
    ViewSet for CRUD operations on movies.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def list(self, request):
        """List all movies"""
        movies = Movie.objects.all()
        data = [{
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'release_date': movie.release_date,
            'duration': movie.duration
        } for movie in movies]
        return Response(data)
    
    def create(self, request):
        """Create a new movie"""
        try:
            movie = Movie.objects.create(
                title=request.data.get('title'),
                description=request.data.get('description'),
                release_date=request.data.get('release_date'),
                duration=request.data.get('duration')
            )
            return Response({
                'id': movie.id,
                'title': movie.title,
                'description': movie.description,
                'release_date': movie.release_date,
                'duration': movie.duration
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """Get a specific movie"""
        try:
            movie = Movie.objects.get(pk=pk)
            return Response({
                'id': movie.id,
                'title': movie.title,
                'description': movie.description,
                'release_date': movie.release_date,
                'duration': movie.duration
            })
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        """Update a movie"""
        try:
            movie = Movie.objects.get(pk=pk)
            movie.title = request.data.get('title', movie.title)
            movie.description = request.data.get('description', movie.description)
            movie.release_date = request.data.get('release_date', movie.release_date)
            movie.duration = request.data.get('duration', movie.duration)
            movie.save()
            return Response({
                'id': movie.id,
                'title': movie.title,
                'description': movie.description,
                'release_date': movie.release_date,
                'duration': movie.duration
            })
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def partial_update(self, request, pk=None):
        """Partially update a movie"""
        return self.update(request, pk)
    
    def destroy(self, request, pk=None):
        """Delete a movie"""
        try:
            movie = Movie.objects.get(pk=pk)
            movie.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'])
    def available_seats(self, request, pk=None):
        """Get all available seats for a specific movie"""
        try:
            movie = Movie.objects.get(pk=pk)
            booked_seats = Booking.objects.filter(movie=movie).values_list('seat_id', flat=True)
            available_seats = Seat.objects.exclude(id__in=booked_seats)
            data = [{
                'id': seat.id,
                'seat_number': seat.seat_number,
                'is_booked': seat.is_booked
            } for seat in available_seats]
            return Response(data)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)


class SeatViewSet(viewsets.ViewSet):
    """
    ViewSet for seat availability and booking status.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def list(self, request):
        """List all seats"""
        seats = Seat.objects.all()
        data = [{
            'id': seat.id,
            'seat_number': seat.seat_number,
            'is_booked': seat.is_booked
        } for seat in seats]
        return Response(data)
    
    def create(self, request):
        """Create a new seat"""
        try:
            seat = Seat.objects.create(
                seat_number=request.data.get('seat_number'),
                is_booked=request.data.get('is_booked', False)
            )
            return Response({
                'id': seat.id,
                'seat_number': seat.seat_number,
                'is_booked': seat.is_booked
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """Get a specific seat"""
        try:
            seat = Seat.objects.get(pk=pk)
            return Response({
                'id': seat.id,
                'seat_number': seat.seat_number,
                'is_booked': seat.is_booked
            })
        except Seat.DoesNotExist:
            return Response({'error': 'Seat not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        """Update a seat"""
        try:
            seat = Seat.objects.get(pk=pk)
            seat.seat_number = request.data.get('seat_number', seat.seat_number)
            seat.is_booked = request.data.get('is_booked', seat.is_booked)
            seat.save()
            return Response({
                'id': seat.id,
                'seat_number': seat.seat_number,
                'is_booked': seat.is_booked
            })
        except Seat.DoesNotExist:
            return Response({'error': 'Seat not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def partial_update(self, request, pk=None):
        """Partially update a seat"""
        return self.update(request, pk)
    
    def destroy(self, request, pk=None):
        """Delete a seat"""
        try:
            seat = Seat.objects.get(pk=pk)
            seat.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Seat.DoesNotExist:
            return Response({'error': 'Seat not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all available seats"""
        movie_id = request.query_params.get('movie_id', None)
        
        if movie_id:
            # Get seats not booked for a specific movie
            booked_seats = Booking.objects.filter(movie_id=movie_id).values_list('seat_id', flat=True)
            available_seats = Seat.objects.exclude(id__in=booked_seats)
        else:
            # Get all seats that are not marked as booked
            available_seats = Seat.objects.filter(is_booked=False)
        
        data = [{
            'id': seat.id,
            'seat_number': seat.seat_number,
            'is_booked': seat.is_booked
        } for seat in available_seats]
        return Response(data)
    
    @action(detail=True, methods=['get'])
    def check_availability(self, request, pk=None):
        """Check if a specific seat is available for a movie"""
        try:
            seat = Seat.objects.get(pk=pk)
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
                "seat_number": seat.seat_number,
                "movie_id": movie_id,
                "is_available": is_available
            })
        except Seat.DoesNotExist:
            return Response({'error': 'Seat not found'}, status=status.HTTP_404_NOT_FOUND)


class BookingViewSet(viewsets.ViewSet):
    """
    ViewSet for users to book seats and view their booking history.
    """
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """List current user's bookings (or all if staff)"""
        if request.user.is_staff:
            bookings = Booking.objects.all()
        else:
            bookings = Booking.objects.filter(user=request.user)
        
        data = [{
            'id': booking.id,
            'movie': booking.movie.id,
            'movie_title': booking.movie.title,
            'seat': booking.seat.id,
            'seat_number': booking.seat.seat_number,
            'user': booking.user.username,
            'booking_date': booking.booking_date
        } for booking in bookings]
        return Response(data)
    
    def create(self, request):
        """Create a new booking"""
        try:
            movie_id = request.data.get('movie')
            seat_id = request.data.get('seat')
            
            # Validate input
            if not movie_id or not seat_id:
                return Response(
                    {'error': 'movie and seat are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if booking already exists
            if Booking.objects.filter(movie_id=movie_id, seat_id=seat_id).exists():
                return Response(
                    {'error': 'This seat is already booked for this movie'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            movie = Movie.objects.get(pk=movie_id)
            seat = Seat.objects.get(pk=seat_id)
            
            booking = Booking.objects.create(
                movie=movie,
                seat=seat,
                user=request.user
            )
            
            return Response({
                'id': booking.id,
                'movie': booking.movie.id,
                'movie_title': booking.movie.title,
                'seat': booking.seat.id,
                'seat_number': booking.seat.seat_number,
                'user': booking.user.username,
                'booking_date': booking.booking_date
            }, status=status.HTTP_201_CREATED)
            
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        except Seat.DoesNotExist:
            return Response({'error': 'Seat not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """Get a specific booking"""
        try:
            booking = Booking.objects.get(pk=pk)
            
            # Check permissions
            if booking.user != request.user and not request.user.is_staff:
                return Response(
                    {'error': 'You can only view your own bookings'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            return Response({
                'id': booking.id,
                'movie': booking.movie.id,
                'movie_title': booking.movie.title,
                'seat': booking.seat.id,
                'seat_number': booking.seat.seat_number,
                'user': booking.user.username,
                'booking_date': booking.booking_date
            })
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        """Cancel a booking"""
        try:
            booking = Booking.objects.get(pk=pk)
            
            # Check permissions
            if booking.user != request.user and not request.user.is_staff:
                return Response(
                    {'error': 'You can only cancel your own bookings'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            booking.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        """Get current user's booking history"""
        bookings = Booking.objects.filter(user=request.user)
        data = [{
            'id': booking.id,
            'movie': booking.movie.id,
            'movie_title': booking.movie.title,
            'seat': booking.seat.id,
            'seat_number': booking.seat.seat_number,
            'user': booking.user.username,
            'booking_date': booking.booking_date
        } for booking in bookings]
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get current user's upcoming bookings"""
        bookings = Booking.objects.filter(
            user=request.user,
            movie__release_date__gte=timezone.now().date()
        )
        data = [{
            'id': booking.id,
            'movie': booking.movie.id,
            'movie_title': booking.movie.title,
            'seat': booking.seat.id,
            'seat_number': booking.seat.seat_number,
            'user': booking.user.username,
            'booking_date': booking.booking_date
        } for booking in bookings]
        return Response(data)