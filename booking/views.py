from django.db.models import ExpressionWrapper, F, IntegerField, Count
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
    AstronomyShowRetrieveSerializer,
    ReservationListSerializer
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

        queryset = queryset.select_related("planetarium_dome", "astronomy_show")

        if self.action == "list":
            queryset = queryset.annotate(
                dome_capacity=ExpressionWrapper(
                    F("planetarium_dome__rows") * F("planetarium_dome__seats_in_row"),
                    output_field=IntegerField()
                ),
                tickets_available=ExpressionWrapper(
                    F("planetarium_dome__rows")
                    * F("planetarium_dome__seats_in_row")
                    - Count("tickets"),
                    output_field=IntegerField()
                )
            )

        elif self.action == "retrieve":
            queryset = queryset.prefetch_related("tickets")
        return queryset.distinct()


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.prefetch_related(
        "tickets__show_session__astronomy_show",
        "tickets__show_session__astronomy_show__planetarium_dome"
    )
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer

        return ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
