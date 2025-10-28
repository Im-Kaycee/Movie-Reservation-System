from celery import shared_task
from django.utils import timezone
from .models import Reservation

@shared_task
def expire_unpaid_reservations():
    """Marks unpaid reservations as expired after their payment window passes."""
    now = timezone.now()
    expired = Reservation.objects.filter(
        status='pending_payment',
        expires_at__lt=now
    )
    count = expired.count()
    for res in expired:
        res.status = 'expired'
        res.save()
    return f"{count} reservations expired."
