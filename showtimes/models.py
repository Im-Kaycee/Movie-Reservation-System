from django.db import models
from django.utils import timezone
from movies.models import Movie
from django.contrib.auth.models import User
# Create your models here.

class Auditorium(models.Model):
    name = models.CharField(max_length=100, unique=True)
    total_seats = models.IntegerField()

    def __str__(self):
        return self.name
class Seat(models.Model):
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=100)
    class Meta:
        unique_together = ('auditorium', 'seat_number')
    def __str__(self):
        return f"{self.auditorium.name} - Seat {self.seat_number}"


    
class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE, related_name='showtimes')
    created_at = models.DateTimeField(default=timezone.now)
    status_choices = [
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='scheduled')

    def __str__(self):
        return f"{self.movie.title} at {self.start_time} in {self.auditorium}"

