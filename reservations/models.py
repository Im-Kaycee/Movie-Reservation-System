from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from showtimes.models import Showtime, Seat
from datetime import timedelta

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending_payment', 'Pending Payment'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='reservations')
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_payment')
    expires_at = models.DateTimeField(null=True, blank=True)
    def save(self, *args, **kwargs):
        # Auto-set expiry 10 minutes from creation
        if not self.expires_at:
            self.expires_at = self.created_at + timedelta(minutes=10)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.showtime.movie.title} ({self.showtime.start_time})"

    @property
    def total_seats(self):
        """Returns number of seats reserved for this booking."""
        return self.reserved_seats.count()
class ReservedSeat(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='reserved_seats')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='reserved_instances')

    class Meta:
        unique_together = ('seat', 'reservation')
        constraints = [
            models.UniqueConstraint(
                fields=['seat', 'reservation'],
                name='unique_seat_per_reservation'
            )
        ]

    def __str__(self):
        return f"{self.seat.seat_number} - {self.reservation.showtime.movie.title}"
