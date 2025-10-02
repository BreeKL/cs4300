from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Movie, Seat, Booking
from django.contrib.auth.models import User


def movie_list(request):
    """Display list of all movies"""
    movies = Movie.objects.all().order_by('-release_date')
    return render(request, 'booking/movie_list.html', {
        'movies': movies
    })


def movie_detail(request, pk):
    """Display details of a specific movie"""
    movie = get_object_or_404(Movie, pk=pk)
    
    # Get available seats for this movie
    booked_seats = Booking.objects.filter(movie=movie).values_list('seat_id', flat=True)
    available_seats = Seat.objects.exclude(id__in=booked_seats)
    
    return render(request, 'booking/movie_detail.html', {
        'movie': movie,
        'available_seats': available_seats
    })


def seat_booking(request, movie_id):
    """Display seat booking interface and handle booking submission"""
    movie = get_object_or_404(Movie, pk=movie_id)
    
    if request.method == 'POST':
        seat_ids = request.POST.get('seat_ids', '')
        guest_name = request.POST.get('guest_name', 'Guest').strip()
        
        if not guest_name:
            guest_name = 'Guest'
        
        if not seat_ids:
            messages.error(request, 'Please select at least one seat.')
            return redirect('seat_booking', movie_id=movie_id)
        
        seat_id_list = [int(sid) for sid in seat_ids.split(',') if sid]
        
        # Get or create a guest user (you can modify this logic)
        guest_user, created = User.objects.get_or_create(
            username=f'guest_{guest_name.lower().replace(" ", "_")}',
            defaults={'first_name': guest_name}
        )
        
        # Create bookings for selected seats
        successful_bookings = []
        failed_seats = []
        
        for seat_id in seat_id_list:
            try:
                seat = Seat.objects.get(pk=seat_id)
                
                # Check if seat is already booked for this movie
                if Booking.objects.filter(movie=movie, seat=seat).exists():
                    failed_seats.append(seat.seat_number)
                    continue
                
                # Create booking
                Booking.objects.create(
                    movie=movie,
                    seat=seat,
                    user=guest_user
                )
                successful_bookings.append(seat.seat_number)
                
            except Seat.DoesNotExist:
                continue
        
        # Display appropriate messages
        if successful_bookings:
            seats_str = ', '.join(successful_bookings)
            messages.success(
                request, 
                f'Successfully booked seat(s): {seats_str} for {movie.title}!'
            )
        
        if failed_seats:
            seats_str = ', '.join(failed_seats)
            messages.warning(
                request,
                f'Seat(s) {seats_str} were already booked.'
            )
        
        if not successful_bookings and not failed_seats:
            messages.error(request, 'No valid seats selected.')
            return redirect('seat_booking', movie_id=movie_id)
        
        return redirect('booking_confirmation', movie_id=movie_id)
    
    # GET request - display booking page
    all_seats = Seat.objects.all().order_by('seat_number')
    booked_seats = Booking.objects.filter(movie=movie).values_list('seat_id', flat=True)
    
    return render(request, 'booking/seat_booking.html', {
        'movie': movie,
        'all_seats': all_seats,
        'booked_seat_ids': list(booked_seats)
    })


def booking_confirmation(request, movie_id):
    """Display booking confirmation"""
    movie = get_object_or_404(Movie, pk=movie_id)
    
    return render(request, 'booking/booking_confirmation.html', {
        'movie': movie
    })


def all_bookings(request):
    """Display all bookings (no authentication needed)"""
    bookings = Booking.objects.all().order_by('-booking_date')
    
    # Count upcoming bookings
    today = timezone.now().date()
    upcoming_count = bookings.filter(movie__release_date__gte=today).count()
    
    return render(request, 'booking/all_bookings.html', {
        'bookings': bookings,
        'upcoming_count': upcoming_count,
        'today': today
    })


def cancel_booking(request, booking_id):
    """Cancel a booking (no authentication needed)"""
    if request.method == 'POST':
        booking = get_object_or_404(Booking, pk=booking_id)
        
        # Store info before deleting
        movie_title = booking.movie.title
        seat_number = booking.seat.seat_number
        
        # Delete booking
        booking.delete()
        
        messages.success(
            request,
            f'Successfully cancelled booking for {movie_title}, Seat {seat_number}.'
        )
    
    return redirect('all_bookings')