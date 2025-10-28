from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q

# Create your views here.
class AuditoriumListView(generics.ListAPIView):
    queryset = Auditorium.objects.all()
    serializer_class = AuditoriumSerializer
    permission_classes = [AllowAny]
    
class AuditoriumDetailView(generics.RetrieveAPIView):
    queryset = Auditorium.objects.all()
    serializer_class = AuditoriumDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    

class AvailableSeatsView(generics.ListAPIView):
    """
    GET /showtimes/<showtime_id>/available-seats/
    Returns available seats for the showtime (seats in the auditorium excluding currently reserved ones).
    Response: { "available_count": int, "seats": [ {id, seat_number, auditorium}, ... ] }
    """
    serializer_class = SeatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        showtime_id = self.kwargs.get('showtime_id')
        if not showtime_id:
            raise ValidationError({"showtime_id": "showtime_id path parameter is required."})

        try:
            showtime = Showtime.objects.get(id=showtime_id)
        except Showtime.DoesNotExist:
            raise NotFound("Showtime not found.")

        # all seats in the auditorium
        seats_qs = Seat.objects.filter(auditorium=showtime.auditorium)

        # import here to avoid circular imports if reservations import showtimes
        from reservations.models import ReservedSeat

        # consider seats reserved: include all 'paid' seats,
        # plus 'pending_payment' seats that haven't expired yet
        reserved_qs = ReservedSeat.objects.filter(
            reservation__showtime=showtime
        ).filter(
            Q(reservation__status='paid') |
            (Q(reservation__status='pending_payment') & Q(reservation__expires_at__gte=timezone.now()))
        )
        reserved_ids = reserved_qs.values_list('seat_id', flat=True)

        return seats_qs.exclude(id__in=list(reserved_ids))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "available_count": queryset.count(),
            "seats": serializer.data
        }, status=status.HTTP_200_OK)
