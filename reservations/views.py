from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from datetime import timedelta
from django.utils import timezone
# Create your views here.
class ReservationCreateView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class ReservationListView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.filter(user=user, status='paid')
class CancelledReservationListView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.filter(user=user, status='cancelled')

class ReservationDetailView(generics.RetrieveAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_object(self):
        user = self.request.user
        try:
            reservation = Reservation.objects.get(id=self.kwargs['id'], user=user)
            return reservation
        except Reservation.DoesNotExist:
            raise NotFound("Reservation not found.")
class CancelReservationView(generics.UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        reservation = self.get_object()
        if reservation.status != 'paid':
            return Response({"detail": "Reservation cannot be cancelled."}, status=400)
        reservation.status = 'cancelled'
        reservation.save()
        serializer = self.get_serializer(reservation)
        return Response(serializer.data)
class MockPaymentView(generics.UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        reservation = self.get_object()

        if reservation.status != 'pending_payment':
            return Response(
                {"detail": "Payment not allowed for this reservation."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if timezone.now() > reservation.created_at + timedelta(minutes=10):
            reservation.status = 'expired'
            reservation.save()
            return Response(
                {"detail": "Reservation expired. Please book again."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Simulate successful payment
        reservation.status = 'paid'
        reservation.save()

        return Response({
            "message": "Mock payment successful. Reservation confirmed.",
            "reservation_id": reservation.id,
            "status": reservation.status
        })

