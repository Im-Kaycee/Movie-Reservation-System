from django.urls import path
from .views import ShowtimeListView, MovieDetailView

urlpatterns = [
    path('showtimes/', ShowtimeListView.as_view(), name='showtime-list'),
    path('<int:id>/', MovieDetailView.as_view(), name='movie-detail'),
]