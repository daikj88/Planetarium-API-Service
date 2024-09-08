from django.urls import path, include
from rest_framework import routers

from booking.views import (
    ShowThemeViewSet,
    AstronomyShowViewSet,
    PlanetariumDomeViewSet,
    ShowSessionViewSet,
    ReservationViewSet
)

routers = routers.DefaultRouter()
routers.register("astronomy_shows", AstronomyShowViewSet)
routers.register("planetarium_domes", PlanetariumDomeViewSet)
routers.register("show_themes", ShowThemeViewSet)
routers.register("show_sessions", ShowSessionViewSet)
routers.register("reservations", ReservationViewSet)

urlpatterns = [
    path("", include(routers.urls)),
]

app_name = "booking"
