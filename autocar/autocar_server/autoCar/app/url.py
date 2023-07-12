from django.urls import path
from . import views

urlpatterns = [
    path("stop/", views.last_stopCommand),
    path("traffic_light/", views.last_trafficLightCommand),
]
