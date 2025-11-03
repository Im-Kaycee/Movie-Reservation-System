from django.urls import path
from .views import *

urlpatterns = [
    path('', MovieListView.as_view(), name='movie-list'),
    path('showtimes/', ShowtimeListView.as_view(), name='showtime-list'),
    path('<int:id>/', MovieDetailView.as_view(), name='movie-detail'),
]