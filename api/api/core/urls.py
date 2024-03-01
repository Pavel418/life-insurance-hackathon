from django.urls import path
from .views import TripView

urlpatterns = [
    path('', TripView.as_view(), name='get_weather'), 
]

