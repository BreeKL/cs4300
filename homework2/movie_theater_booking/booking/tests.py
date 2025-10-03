from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from datetime import date, timedelta
from .models import Movie, Seat, Booking


# ==================== MODEL TESTS ====================

class MovieModelTest(TestCase):
    """Unit tests for the Movie model"""
    
    def setUp(self):
        """Set up test data"""
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="A test movie description",
            release_date=date.today() + timedelta(days=7),
            duration=120
        )
    
    def test_movie_creation(self):
        """Test that a movie can be created successfully"""
        self.assertEqual(self.movie.title, "Test Movie")
        self.assertEqual(self.movie.description, "A test movie description")
        self.assertEqual(self.movie.duration, 120)
        self.assertIsNotNone(self.movie.release_date)
    
    def test_movie_str_representation(self):
        """Test the string representation of a movie"""
        self.assertEqual(str(self.movie), "Test Movie")
    
    def test_movie_ordering(self):
        """Test that movies are ordered by release date (newest first)"""
        # Clear existing movies to avoid confusion
        Movie.objects.all().delete()
        
        movie1 = Movie.objects.create(
            title="Movie 1",
            description="Description 1",
            release_date=date.today(),
            duration=90
        )
        movie2 = Movie.objects.create(
            title="Movie 2",
            description="Description 2",
            release_date=date.today() + timedelta(days=1),
            duration=100
        )
        movies = list(Movie.objects.all())
        # First movie should be the newest (movie2)
        self.assertEqual(movies[0], movie2)  # Newest first
        self.assertEqual(movies[1], movie1)
    
    def test_movie_fields(self):
        """Test that all movie fields are correctly set"""
        self.assertIsInstance(self.movie.title, str)
        self.assertIsInstance(self.movie.description, str)
        self.assertIsInstance(self.movie.release_date, date)
        self.assertIsInstance(self.movie.duration, int)


class SeatModelTest(TestCase):
    """Unit tests for the Seat model"""
    
    def setUp(self):
        """Set up test data"""
        self.seat = Seat.objects.create(
            seat_number="A1",
            is_booked=False
        )
    
    def test_seat_creation(self):
        """Test that a seat can be created successfully"""
        self.assertEqual(self.seat.seat_number, "A1")
        self.assertEqual(self.seat.is_booked, False)
    
    def test_seat_str_representation(self):
        """Test the string representation of a seat"""
        self.assertEqual(str(self.seat), "Seat A1")
    
    def test_seat_unique_constraint(self):
        """Test that seat numbers must be unique"""
        with self.assertRaises(Exception):
            Seat.objects.create(seat_number="A1", is_booked=False)
    
    def test_seat_default_is_booked(self):
        """Test that is_booked defaults to False"""
        seat = Seat.objects.create(seat_number="B1")
        self.assertEqual(seat.is_booked, False)
    
    def test_seat_ordering(self):
        """Test that seats are ordered by seat number"""
        Seat.objects.create(seat_number="C1")
        Seat.objects.create(seat_number="B1")
        seats = Seat.objects.all()
        self.assertEqual(seats[0].seat_number, "A1")
        self.assertEqual(seats[1].seat_number, "B1")
        self.assertEqual(seats[2].seat_number, "C1")


class BookingModelTest(TestCase):
    """Unit tests for the Booking model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test Description",
            release_date=date.today() + timedelta(days=7),
            duration=120
        )
        self.seat = Seat.objects.create(seat_number="A1")
        self.booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user
        )
    
    def test_booking_creation(self):
        """Test that a booking can be created successfully"""
        self.assertEqual(self.booking.movie, self.movie)
        self.assertEqual(self.booking.seat, self.seat)
        self.assertEqual(self.booking.user, self.user)
        self.assertIsNotNone(self.booking.booking_date)
    
    def test_booking_str_representation(self):
        """Test the string representation of a booking"""
        expected = f"{self.user.username} - {self.movie.title} - {self.seat.seat_number}"
        self.assertEqual(str(self.booking), expected)
    
    def test_booking_unique_together_constraint(self):
        """Test that the same seat cannot be booked twice for the same movie"""
        with self.assertRaises(Exception):
            Booking.objects.create(
                movie=self.movie,
                seat=self.seat,
                user=self.user
            )
    
    def test_booking_different_movies_same_seat(self):
        """Test that the same seat can be booked for different movies"""
        movie2 = Movie.objects.create(
            title="Movie 2",
            description="Description 2",
            release_date=date.today() + timedelta(days=14),
            duration=100
        )
        booking2 = Booking.objects.create(
            movie=movie2,
            seat=self.seat,
            user=self.user
        )
        self.assertIsNotNone(booking2)
    
    def test_booking_cascade_delete_movie(self):
        """Test that deleting a movie deletes its bookings"""
        booking_id = self.booking.id
        self.movie.delete()
        with self.assertRaises(Booking.DoesNotExist):
            Booking.objects.get(id=booking_id)
    
    def test_booking_cascade_delete_seat(self):
        """Test that deleting a seat deletes its bookings"""
        booking_id = self.booking.id
        self.seat.delete()
        with self.assertRaises(Booking.DoesNotExist):
            Booking.objects.get(id=booking_id)
    
    def test_booking_cascade_delete_user(self):
        """Test that deleting a user deletes their bookings"""
        booking_id = self.booking.id
        self.user.delete()
        with self.assertRaises(Booking.DoesNotExist):
            Booking.objects.get(id=booking_id)


# ==================== API INTEGRATION TESTS ====================

@override_settings(FORCE_SCRIPT_NAME=None)
class MovieAPITest(APITestCase):
    """Integration tests for Movie API endpoints"""
    
    def setUp(self):
        """Set up test data and API client"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test Description",
            release_date=date.today() + timedelta(days=7),
            duration=120
        )
    
    def test_list_movies(self):
        """Test GET /api/movies/ returns list of movies"""
        url = reverse('api-movie-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Test Movie")
    
    def test_retrieve_movie(self):
        """Test GET /api/movies/{id}/ returns a specific movie"""
        url = reverse('api-movie-detail', args=[self.movie.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Movie")
        self.assertEqual(response.data['duration'], 120)
    
    def test_retrieve_nonexistent_movie(self):
        """Test GET /api/movies/{invalid_id}/ returns 404"""
        url = reverse('api-movie-detail', args=[9999])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_movie(self):
        """Test POST /api/movies/ creates a new movie"""
        self.client.force_authenticate(user=self.user)  # Authenticate for write operations
        url = reverse('api-movie-list')
        data = {
            'title': 'New Movie',
            'description': 'New Description',
            'release_date': str(date.today() + timedelta(days=14)),
            'duration': 150
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Movie')
        self.assertEqual(Movie.objects.count(), 2)
    
    def test_update_movie(self):
        """Test PUT /api/movies/{id}/ updates a movie"""
        self.client.force_authenticate(user=self.user)  # Authenticate for write operations
        url = reverse('api-movie-detail', args=[self.movie.id])
        data = {
            'title': 'Updated Movie',
            'description': 'Updated Description',
            'release_date': str(date.today() + timedelta(days=14)),
            'duration': 130
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Movie')
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, 'Updated Movie')
    
    def test_delete_movie(self):
        """Test DELETE /api/movies/{id}/ deletes a movie"""
        self.client.force_authenticate(user=self.user)  # Authenticate for write operations
        url = reverse('api-movie-detail', args=[self.movie.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 0)
    
    def test_movie_available_seats(self):
        """Test GET /api/movies/{id}/available_seats/ returns available seats"""
        seat1 = Seat.objects.create(seat_number="A1")
        seat2 = Seat.objects.create(seat_number="A2")
        
        url = reverse('api-movie-available-seats', args=[self.movie.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class SeatAPITest(APITestCase):
    """Integration tests for Seat API endpoints"""
    
    def setUp(self):
        """Set up test data and API client"""
        self.client = APIClient()
        self.seat = Seat.objects.create(seat_number="A1", is_booked=False)
    
    def test_list_seats(self):
        """Test GET /api/seats/ returns list of seats"""
        url = reverse('api-seat-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
    
    def test_retrieve_seat(self):
        """Test GET /api/seats/{id}/ returns a specific seat"""
        url = reverse('api-seat-detail', args=[self.seat.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['seat_number'], "A1")
    
    def test_create_seat(self):
        """Test POST /api/seats/ creates a new seat"""
        self.client.force_authenticate(user=User.objects.create_user(username='testuser', password='pass'))
        url = reverse('api-seat-list')
        data = {
            'seat_number': 'B1',
            'is_booked': False
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['seat_number'], 'B1')
        self.assertEqual(Seat.objects.count(), 2)
    
    def test_update_seat(self):
        """Test PUT /api/seats/{id}/ updates a seat"""
        self.client.force_authenticate(user=User.objects.create_user(username='testuser', password='pass'))
        url = reverse('api-seat-detail', args=[self.seat.id])
        data = {
            'seat_number': 'A1',
            'is_booked': True
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_booked'], True)
    
    def test_delete_seat(self):
        """Test DELETE /api/seats/{id}/ deletes a seat"""
        self.client.force_authenticate(user=User.objects.create_user(username='testuser', password='pass'))
        url = reverse('api-seat-detail', args=[self.seat.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Seat.objects.count(), 0)
    
    def test_available_seats_no_movie(self):
        """Test GET /api/seats/available/ returns available seats"""
        Seat.objects.create(seat_number="B1", is_booked=False)
        Seat.objects.create(seat_number="C1", is_booked=True)
        
        url = reverse('api-seat-available')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Only non-booked seats
    
    def test_available_seats_for_movie(self):
        """Test GET /api/seats/available/?movie_id={id} returns seats available for a movie"""
        movie = Movie.objects.create(
            title="Test Movie",
            description="Test",
            release_date=date.today(),
            duration=120
        )
        seat1 = Seat.objects.create(seat_number="B1")
        seat2 = Seat.objects.create(seat_number="C1")
        user = User.objects.create_user(username="testuser", password="pass")
        
        # Book seat1 for the movie
        Booking.objects.create(movie=movie, seat=seat1, user=user)
        
        url = reverse('api-seat-available')
        response = self.client.get(url, {'movie_id': movie.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return A1 and C1 (B1 is booked for this movie)
        seat_numbers = [seat['seat_number'] for seat in response.data]
        self.assertIn('A1', seat_numbers)
        self.assertIn('C1', seat_numbers)
        self.assertNotIn('B1', seat_numbers)
    
    def test_check_seat_availability(self):
        """Test GET /api/seats/{id}/check_availability/?movie_id={id}"""
        movie = Movie.objects.create(
            title="Test Movie",
            description="Test",
            release_date=date.today(),
            duration=120
        )
        
        url = reverse('api-seat-check-availability', args=[self.seat.id])
        response = self.client.get(url, {'movie_id': movie.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_available'], True)


class BookingAPITest(APITestCase):
    """Integration tests for Booking API endpoints"""
    
    def setUp(self):
        """Set up test data and API client"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.force_authenticate(user=self.user)
        
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test Description",
            release_date=date.today() + timedelta(days=7),
            duration=120
        )
        self.seat = Seat.objects.create(seat_number="A1")
        self.booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user
        )
    
    def test_list_bookings_authenticated(self):
        """Test GET /api/bookings/ returns user's bookings"""
        url = reverse('api-booking-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
    
    def test_list_bookings_unauthenticated(self):
        """Test GET /api/bookings/ requires authentication"""
        self.client.force_authenticate(user=None)
        url = reverse('api-booking-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_booking(self):
        """Test POST /api/bookings/ creates a new booking"""
        seat2 = Seat.objects.create(seat_number="A2")
        url = reverse('api-booking-list')
        data = {
            'movie': self.movie.id,
            'seat': seat2.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['seat_number'], 'A2')
        self.assertEqual(Booking.objects.count(), 2)
    
    def test_create_duplicate_booking(self):
        """Test POST /api/bookings/ prevents duplicate bookings"""
        url = reverse('api-booking-list')
        data = {
            'movie': self.movie.id,
            'seat': self.seat.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check for either our custom message or Django's unique constraint message
        response_str = str(response.data)
        self.assertTrue(
            'already booked' in response_str.lower() or 'unique' in response_str.lower(),
            f"Expected duplicate booking error, got: {response_str}"
        )
    
    def test_retrieve_booking(self):
        """Test GET /api/bookings/{id}/ returns a specific booking"""
        url = reverse('api-booking-detail', args=[self.booking.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['movie_title'], "Test Movie")
        self.assertEqual(response.data['seat_number'], "A1")
    
    def test_retrieve_other_user_booking(self):
        """Test GET /api/bookings/{id}/ prevents viewing other users' bookings"""
        other_user = User.objects.create_user(
            username="otheruser",
            password="pass123"
        )
        seat2 = Seat.objects.create(seat_number="A2")
        other_booking = Booking.objects.create(
            movie=self.movie,
            seat=seat2,
            user=other_user
        )
        
        url = reverse('api-booking-detail', args=[other_booking.id])
        response = self.client.get(url)
        
        # The queryset is filtered by get_queryset(), so it returns 404 instead of 403
        # This is actually more secure as it doesn't reveal the existence of the booking
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_booking(self):
        """Test DELETE /api/bookings/{id}/ deletes a booking"""
        url = reverse('api-booking-detail', args=[self.booking.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 0)
    
    def test_my_bookings(self):
        """Test GET /api/bookings/my_bookings/ returns user's bookings"""
        url = reverse('api-booking-my-bookings')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_upcoming_bookings(self):
        """Test GET /api/bookings/upcoming/ returns upcoming bookings"""
        url = reverse('api-booking-upcoming')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


# ==================== TEMPLATE VIEW TESTS ====================

class TemplateViewsTest(TestCase):
    """Integration tests for template-based views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test Description",
            release_date=date.today() + timedelta(days=7),
            duration=120
        )
        self.seat = Seat.objects.create(seat_number="A1")
    
    def test_movie_list_view(self):
        """Test movie list page renders correctly"""
        response = self.client.get(reverse('movie_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/movie_list.html')
        self.assertContains(response, "Test Movie")
    
    def test_movie_detail_view(self):
        """Test movie detail page renders correctly"""
        response = self.client.get(reverse('movie_detail', args=[self.movie.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/movie_detail.html')
        self.assertContains(response, "Test Movie")
    
    def test_seat_booking_view_get(self):
        """Test seat booking page renders correctly"""
        response = self.client.get(reverse('seat_booking', args=[self.movie.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/seat_booking.html')
        self.assertContains(response, "A1")
    
    def test_seat_booking_view_post(self):
        """Test booking creation via POST"""
        response = self.client.post(
            reverse('seat_booking', args=[self.movie.id]),
            {
                'seat_ids': str(self.seat.id),
                'guest_name': 'Test User'
            }
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Booking.objects.count(), 1)
    
    def test_all_bookings_view(self):
        """Test all bookings page renders correctly"""
        user = User.objects.create_user(username="testuser", password="pass")
        Booking.objects.create(movie=self.movie, seat=self.seat, user=user)
        
        response = self.client.get(reverse('all_bookings'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/all_bookings.html')
        self.assertContains(response, "Test Movie")
    
    def test_cancel_booking(self):
        """Test booking cancellation"""
        user = User.objects.create_user(username="testuser", password="pass")
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=user)
        
        response = self.client.post(reverse('cancel_booking', args=[booking.id]))
        
        self.assertEqual(response.status_code, 302)  # Redirect after cancel
        self.assertEqual(Booking.objects.count(), 0)