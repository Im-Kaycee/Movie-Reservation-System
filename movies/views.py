from django.shortcuts import render
from .models import Movie
from showtimes.serializers import ShowtimeSerializer
from showtimes.models import Showtime
from .serializers import MovieSerializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotFound
class ShowtimeListView(generics.ListAPIView):
    serializer_class = ShowtimeSerializer
    permission_classes = [IsAuthenticated]
    #GET /showtimes/?movie=1&date=2025-10-27
    #GET /showtimes/?date=2025-10-27
    #GET /showtimes/
    #GET /showtimes/?movie=1
    def get_queryset(self):
        qs = Showtime.objects.all().order_by('start_time')
        params = self.request.query_params

        # Get date parameters
        date = params.get('date')
        date_from = params.get('from')
        date_to = params.get('to')
        movie_id = params.get('movie')

        try:
            # Filter by specific date
            if date:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                qs = qs.filter(
                    start_time__date=date_obj.date()
                )

            # Filter by date range
            if date_from:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
                qs = qs.filter(start_time__date__gte=date_from_obj.date())
            
            if date_to:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
                qs = qs.filter(start_time__date__lte=date_to_obj.date())

            # Filter by movie if provided
            if movie_id:
                qs = qs.filter(movie_id=movie_id)

            # Only show future and ongoing showtimes by default
            if not any([date, date_from, date_to]):
                qs = qs.filter(end_time__gte=timezone.now())
            if not qs.exists():
                raise NotFound(detail="Showtimes not found.")

            return qs

        except ValueError:
            raise ValidationError({
                "error": "Invalid date format. Use YYYY-MM-DD"
            })

class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    def get_object(self):
        try:
            return self.queryset.get(id=self.kwargs['id'])
        except Movie.DoesNotExist:
            raise NotFound(detail="Movie not found.")