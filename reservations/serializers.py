from rest_framework import serializers
from .models import *
from main.serializers import UserSerializer
from showtimes.serializers import ShowtimeSerializer, SeatSerializer
from django.db import transaction
from datetime import timedelta
from django.utils import timezone  
class ReservedSeatSerializer(serializers.ModelSerializer):
    seat_number = serializers.CharField(source='seat.seat_number', read_only=True)


    class Meta:
        model = ReservedSeat
        fields = ['seat_number']

class ReservationSerializer(serializers.ModelSerializer):
    showtime = ShowtimeSerializer(read_only=True)
    showtime_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    reserved_seats = ReservedSeatSerializer(many=True, read_only=True)
    seats = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=True
    )
    is_cancellable = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'showtime', 'showtime_id', 'created_at', 'status', 
                 'reserved_seats', 'is_cancellable', 'seats']

    def get_is_cancellable(self, obj):
        cancellation_window = timedelta(hours=1)
        if not obj or not getattr(obj, 'showtime', None):
            return False
        return obj.showtime.start_time > (timezone.now() + cancellation_window)
        
    @transaction.atomic
    def create(self, validated_data):
        seats_data = validated_data.pop('seats', [])
        showtime_id = validated_data.pop('showtime_id')
        
        try:
            showtime = Showtime.objects.get(id=showtime_id)
        except Showtime.DoesNotExist:
            raise serializers.ValidationError({"showtime": "Showtime not found"})

        # Validate seats exist
        seats = Seat.objects.filter(id__in=seats_data)
        if len(seats) != len(seats_data):
            raise serializers.ValidationError({"seats": "One or more seats not found"})

        # Check seats belong to showtime's auditorium
        invalid_seats = seats.exclude(auditorium=showtime.auditorium)
        if invalid_seats.exists():
            raise serializers.ValidationError({
                "seats": f"Seats {list(invalid_seats.values_list('seat_number', flat=True))} "
                        f"don't belong to auditorium {showtime.auditorium.name}"
            })

        unavailable_seats = ReservedSeat.objects.filter(
            seat__in=seats,
            reservation__showtime=showtime,
            reservation__status__in=['active', 'paid', 'pending_payment']
        ).exclude(reservation__expires_at__lt=timezone.now())

        if unavailable_seats.exists():
            taken_seats = list(unavailable_seats.values_list('seat__seat_number', flat=True))
            raise serializers.ValidationError({
                "seats": f"Seats {taken_seats} are already reserved"
            })

        validated_data['showtime'] = showtime
        reservation = Reservation.objects.create(
            **validated_data,
            status='pending_payment',
            expires_at=timezone.now() + timedelta(minutes=10)
)


        # Create reserved seats
        ReservedSeat.objects.bulk_create([
            ReservedSeat(
                reservation=reservation,
                seat=seat
            ) for seat in seats
        ])

        return reservation