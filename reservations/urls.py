from .models import *
from .serializers import *
from .views import *

from django.urls import path
urlpatterns = [
    path('', ReservationListView.as_view(), name='reservation-list'),
    path('create/', ReservationCreateView.as_view(), name='reservation-create'),
    path('<int:id>/', ReservationDetailView.as_view(), name='reservation-detail'),
    path('<int:id>/cancel/', CancelReservationView.as_view(), name='reservation-cancel'),
    path('cancelled/', CancelledReservationListView.as_view(), name='cancelled-reservation-list'),
    path('<int:id>/mock-payment/', MockPaymentView.as_view(), name='mock-payment'),
]