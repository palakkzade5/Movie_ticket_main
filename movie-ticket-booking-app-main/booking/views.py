from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
from .models import Show
from django.core.mail import send_mail
from django.conf import settings

class RegisterView(View):
    def get(self, request):
        return render(request, 'booking/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not username or not email or not password or not password2:
            messages.error(request, 'Please fill all fields')
            return redirect('booking:register')

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('booking:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('booking:register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Registration successful. Please login.')
        return redirect('booking:login')

class LoginView(View):
    def get(self, request):
        return render(request, 'booking/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('booking:show_list')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('booking:login')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('booking:login')

from django.utils import timezone

class ShowListView(ListView):
    model = Show
    template_name = 'booking/show_list.html'
    context_object_name = 'shows'
    paginate_by = 10

    def get_queryset(self):
        now = timezone.now()
        return Show.objects.filter(
            date__gte=now.date()
        ).order_by('date', 'time')

from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Booking, Seat
from django.contrib.auth.mixins import LoginRequiredMixin

class BookingView(LoginRequiredMixin, View):
    def get(self, request, show_id):
        show = Show.objects.get(id=show_id)
        seats = show.seats.all().order_by('seat_number')
        context = {
            'show': show,
            'seats': seats,
        }
        return render(request, 'booking/booking.html', context)

    def post(self, request, show_id):
        show = Show.objects.get(id=show_id)
        seats_str = request.POST.get('seats', '')
        selected_seat_ids = seats_str.split(',') if seats_str else []
        if not selected_seat_ids or selected_seat_ids == ['']:
            messages.error(request, 'Please select at least one seat.')
            return HttpResponseRedirect(reverse('booking:booking', args=[show_id]))

        seats = Seat.objects.filter(id__in=selected_seat_ids, show=show, is_booked=False)
        if seats.count() != len(selected_seat_ids):
            messages.error(request, 'Some selected seats are already booked.')
            return HttpResponseRedirect(reverse('booking:booking', args=[show_id]))

        booking = Booking.objects.create(user=request.user, show=show, confirmed=True)
        booking.seats.set(seats)
        booking.save()

        seats.update(is_booked=True)
        show.available_seats -= seats.count()
        show.save()

        # Send booking confirmation email
        subject = 'Booking Confirmation'
        message = f'Dear {request.user.username},\n\nYour booking for {show.movie.title} on {show.date} at {show.time} has been confirmed.\n\nThank you for using our service!'
        from_email = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@example.com'
        recipient_list = [request.user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)

        messages.success(request, 'Booking confirmed! A confirmation email has been sent.')
        return HttpResponseRedirect(reverse('booking:booking_history'))

class BookingHistoryView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking/booking_history.html'
    context_object_name = 'bookings'
    paginate_by = 10

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-booking_date')
