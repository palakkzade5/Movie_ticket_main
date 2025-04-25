from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from .models import Show, Booking, Movie
from django.urls import reverse

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class MovieListAdminView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request):
        movies = Movie.objects.all().order_by('title')
        return render(request, 'booking/admin_movie_list.html', {'movies': movies})

class MovieCreateView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request):
        return render(request, 'booking/admin_movie_form.html')

    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        duration = request.POST.get('duration')
        genre = request.POST.get('genre')
        director = request.POST.get('director')
        release_date = request.POST.get('release_date')
        poster = request.FILES.get('poster')

        if not all([title, duration]):
            messages.error(request, 'Please fill all required fields.')
            return redirect('booking:admin_movie_create')

        movie = Movie.objects.create(
            title=title,
            description=description,
            duration=int(duration),
            genre=genre,
            director=director,
            release_date=release_date if release_date else None,
            poster=poster
        )
        messages.success(request, 'Movie created successfully.')
        return redirect('booking:admin_movie_list')

class MovieEditView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        return render(request, 'booking/admin_movie_form.html', {'movie': movie})

    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        title = request.POST.get('title')
        description = request.POST.get('description')
        duration = request.POST.get('duration')
        genre = request.POST.get('genre')
        director = request.POST.get('director')
        release_date = request.POST.get('release_date')
        poster = request.FILES.get('poster')

        if not all([title, duration]):
            messages.error(request, 'Please fill all required fields.')
            return redirect('booking:admin_movie_edit', movie_id=movie_id)

        movie.title = title
        movie.description = description
        movie.duration = int(duration)
        movie.genre = genre
        movie.director = director
        movie.release_date = release_date if release_date else None
        if poster:
            movie.poster = poster
        movie.save()
        messages.success(request, 'Movie updated successfully.')
        return redirect('booking:admin_movie_list')

class MovieDeleteView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        movie.delete()
        messages.success(request, 'Movie deleted successfully.')
        return redirect('booking:admin_movie_list')

class ShowListAdminView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request):
        shows = Show.objects.all().order_by('date', 'time')
        return render(request, 'booking/admin_show_list.html', {'shows': shows})

class ShowCreateView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request):
        movies = Movie.objects.all().order_by('title')
        return render(request, 'booking/admin_show_form.html', {'movies': movies})

    def post(self, request):
        movie_id = request.POST.get('movie')
        date = request.POST.get('date')
        time = request.POST.get('time')
        venue = request.POST.get('venue')
        total_seats = request.POST.get('total_seats')

        if not all([movie_id, date, time, venue, total_seats]):
            messages.error(request, 'Please fill all required fields.')
            return redirect('booking:admin_show_create')

        movie = get_object_or_404(Movie, id=movie_id)

        show = Show.objects.create(
            movie=movie,
            date=date,
            time=time,
            venue=venue,
            total_seats=int(total_seats),
            available_seats=int(total_seats)
        )

        # Create Seat objects for the show
        seats = []
        for i in range(1, int(total_seats) + 1):
            seat_number = str(i)
            seats.append(Seat(show=show, seat_number=seat_number))
        Seat.objects.bulk_create(seats)

        messages.success(request, 'Show created successfully.')
        return redirect('booking:admin_show_list')

class ShowEditView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        movies = Movie.objects.all().order_by('title')
        return render(request, 'booking/admin_show_form.html', {'show': show, 'movies': movies})

    def post(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        movie_id = request.POST.get('movie')
        date = request.POST.get('date')
        time = request.POST.get('time')
        venue = request.POST.get('venue')
        total_seats = request.POST.get('total_seats')

        if not all([movie_id, date, time, venue, total_seats]):
            messages.error(request, 'Please fill all required fields.')
            return redirect('booking:admin_show_edit', show_id=show_id)

        movie = get_object_or_404(Movie, id=movie_id)

        diff = int(total_seats) - show.total_seats

        show.movie = movie
        show.date = date
        show.time = time
        show.venue = venue
        show.total_seats = int(total_seats)
        show.available_seats += diff
        if show.available_seats < 0:
            show.available_seats = 0
        show.save()

        # Update Seat objects if total_seats changed
        current_seat_count = show.seats.count()
        if int(total_seats) > current_seat_count:
            seats_to_add = int(total_seats) - current_seat_count
            seats = []
            for i in range(current_seat_count + 1, int(total_seats) + 1):
                seat_number = str(i)
                seats.append(Seat(show=show, seat_number=seat_number))
            Seat.objects.bulk_create(seats)
        elif int(total_seats) < current_seat_count:
            seats_to_remove = current_seat_count - int(total_seats)
            seats_to_delete = show.seats.filter(is_booked=False).order_by('-seat_number')[:seats_to_remove]
            seats_to_delete.delete()

        messages.success(request, 'Show updated successfully.')
        return redirect('booking:admin_show_list')

class ShowDeleteView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        show.delete()
        messages.success(request, 'Show deleted successfully.')
        return redirect('booking:admin_show_list')

class BookingListAdminView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request):
        bookings = Booking.objects.all().order_by('-booking_date')
        return render(request, 'booking/admin_booking_list.html', {'bookings': bookings})
