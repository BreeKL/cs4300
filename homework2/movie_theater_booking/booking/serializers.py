from rest_framework import serializers
from .models import Movie, Seat, Booking
from django.contrib.auth.models import User


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for Movie model"""
    
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'duration']
        read_only_fields = ['id']
    
    def validate_duration(self, value):
        """Ensure duration is positive"""
        if value <= 0:
            raise serializers.ValidationError("Duration must be a positive number.")
        return value


class SeatSerializer(serializers.ModelSerializer):
    """Serializer for Seat model"""
    
    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'is_booked']
        read_only_fields = ['id']
    
    def validate_seat_number(self, value):
        """Ensure seat number is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Seat number cannot be empty.")
        return value.strip()


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model with read-only nested fields"""
    
    # Read-only fields for displaying related data
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    seat_number = serializers.CharField(source='seat.seat_number', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 
            'movie', 
            'seat', 
            'user',
            'movie_title',
            'seat_number', 
            'user_username',
            'booking_date'
        ]
        read_only_fields = ['id', 'user', 'booking_date']
    
    def validate(self, data):
        """
        Check that the seat is not already booked for this movie
        """
        movie = data.get('movie')
        seat = data.get('seat')
        
        # For updates, exclude the current instance
        instance = getattr(self, 'instance', None)
        
        query = Booking.objects.filter(movie=movie, seat=seat)
        if instance:
            query = query.exclude(pk=instance.pk)
        
        if query.exists():
            raise serializers.ValidationError(
                "This seat is already booked for this movie."
            )
        
        return data
    
    def create(self, validated_data):
        """Override create to set the user from the request context"""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)


class BookingCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating bookings"""
    
    class Meta:
        model = Booking
        fields = ['movie', 'seat']
    
    def validate(self, data):
        """Check that the seat is not already booked for this movie"""
        movie = data.get('movie')
        seat = data.get('seat')
        
        if Booking.objects.filter(movie=movie, seat=seat).exists():
            raise serializers.ValidationError(
                "This seat is already booked for this movie."
            )
        
        return data
    
    def create(self, validated_data):
        """Set the user from the request context"""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)


class MovieDetailSerializer(MovieSerializer):
    """Extended serializer for movie details with available seats count"""
    
    available_seats_count = serializers.SerializerMethodField()
    total_bookings = serializers.SerializerMethodField()
    
    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + ['available_seats_count', 'total_bookings']
    
    def get_available_seats_count(self, obj):
        """Get count of available seats for this movie"""
        booked_seats = Booking.objects.filter(movie=obj).count()
        total_seats = Seat.objects.count()
        return total_seats - booked_seats
    
    def get_total_bookings(self, obj):
        """Get total number of bookings for this movie"""
        return Booking.objects.filter(movie=obj).count()


class SeatAvailabilitySerializer(serializers.ModelSerializer):
    """Serializer for seat availability with booking status"""
    
    is_available_for_movie = serializers.SerializerMethodField()
    
    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'is_booked', 'is_available_for_movie']
    
    def get_is_available_for_movie(self, obj):
        """Check if seat is available for a specific movie (from context)"""
        movie_id = self.context.get('movie_id')
        if movie_id:
            return not Booking.objects.filter(movie_id=movie_id, seat=obj).exists()
        return not obj.is_booked