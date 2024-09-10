from rest_framework import viewsets

from booking.models import (
    AstronomyShow,
    PlanetariumDome,
    ShowTheme,
    ShowSession,
    Ticket,
    Reservation
)
from booking.serializers import (
    AstronomyShowSerializer,
    PlanetariumDomeSerializer,
    ShowThemeSerializer,
    TicketSerializer,
    ReservationSerializer,
    ShowSessionSerializer,
    ShowSessionListSerializer,
    ShowSessionRetrieveSerializer,
    AstronomyShowListSerializer,
    AstronomyShowRetrieveSerializer
)


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return AstronomyShowListSerializer
        elif self.action == "retrieve":
            return AstronomyShowRetrieveSerializer
        else:
            return AstronomyShowSerializer

    def get_queryset(self):
        queryset = self.queryset

        show_theme = self.request.query_params.get("show_theme")
        if show_theme:
            queryset = queryset.filter(show_theme__id_in=show_theme)

        if self.action in ["list", "retrieve"]:
            return queryset.prefetch_related("show_theme")
        else:
            return queryset.distinct()


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer
        elif self.action == "retrieve":
            return ShowSessionRetrieveSerializer
        else:
            return ShowSessionSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == ["list", "retrieve"]:
            return queryset.select_related()
        else:
            return queryset


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
