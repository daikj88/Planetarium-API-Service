from django.urls import path, include
from rest_framework import routers


routers = routers.DefaultRouter()

urlpatterns = [
    path("", include(routers.urls)),
]

app_name = "booking"
