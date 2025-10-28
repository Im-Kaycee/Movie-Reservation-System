from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from movies.models import Movie

class ShowtimeSerializer(serializers.ModelSerializer):
    movie = serializers.CharField(source='movie.title', read_only=True)
    auditorium = serializers.CharField(source='auditorium.name', read_only=True)

    class Meta:
        model = Showtime
        fields = '__all__'
    def validate(self, data):
        if data['end_time'] <= data['start_time']:
            raise serializers.ValidationError("End time must be after start time")
        
        # Check for overlapping showtimes in same auditorium
        overlapping = Showtime.objects.filter(
            auditorium=data['auditorium'],
            start_time__lt=data['end_time'],
            end_time__gt=data['start_time']
        )
        if self.instance:
            overlapping = overlapping.exclude(pk=self.instance.pk)
        if overlapping.exists():
            raise serializers.ValidationError("This time slot overlaps with another showtime")
        return data
        
        
class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'auditorium']
        
class AuditoriumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditorium
        fields = ['id', 'name', 'total_seats']
class AuditoriumDetailSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)
    class Meta:
        model = Auditorium
        fields = ['id', 'name', 'seats','total_seats']