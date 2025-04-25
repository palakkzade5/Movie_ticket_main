from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    genre = models.CharField(max_length=100, blank=True)
    director = models.CharField(max_length=100, blank=True)
    release_date = models.DateField(null=True, blank=True)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)

    def __str__(self):
        return self.title

class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=200)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.movie.title} at {self.venue} on {self.date} {self.time}"

class Seat(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.seat_number} for {self.show.movie.title}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='bookings')
    seats = models.ManyToManyField(Seat)
    booking_date = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.show.movie.title} on {self.booking_date}"
