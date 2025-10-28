from .views import *
from django.urls import path, include

urlpatterns = [
    path('auditoriums/', AuditoriumListView.as_view(), name='auditorium-list'),
    path('auditoriums/<int:id>/', AuditoriumDetailView.as_view(), name='auditorium-detail'),
    path('<int:showtime_id>/available-seats/', AvailableSeatsView.as_view(), name='available-seats'),
]