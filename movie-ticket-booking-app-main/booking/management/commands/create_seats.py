from django.core.management.base import BaseCommand
from booking.models import Show, Seat

class Command(BaseCommand):
    help = 'Create Seat objects for shows that do not have seats'

    def handle(self, *args, **options):
        shows = Show.objects.all()
        for show in shows:
            seat_count = show.seats.count()
            if seat_count < show.total_seats:
                seats_to_create = show.total_seats - seat_count
                seats = []
                start_num = seat_count + 1
                for i in range(start_num, show.total_seats + 1):
                    seat_number = str(i)
                    seats.append(Seat(show=show, seat_number=seat_number))
                Seat.objects.bulk_create(seats)
                self.stdout.write(self.style.SUCCESS(f'Created {seats_to_create} seats for show {show.id}'))
            else:
                self.stdout.write(f'Show {show.id} already has {seat_count} seats')
