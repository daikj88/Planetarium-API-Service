from django.db.models import ExpressionWrapper, F, IntegerField, Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from booking.models import (
    AstronomyShow,
    PlanetariumDome,
    ShowTheme,
    ShowSession,
    Reservation
)
from booking.permissions import IsAdminOrIfAuthenticatedReadOnly
from booking.serializers import (
    AstronomyShowSerializer,
    PlanetariumDomeSerializer,
    ShowThemeSerializer,
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
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

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
            show_theme_ids = [int(id.strip()) for id in show_theme.split(',')]
            queryset = queryset.filter(show_theme__id__in=show_theme_ids)

        if self.action in ["list", "retrieve"]:
            return queryset.prefetch_related("show_theme")
        else:
            return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "show_theme",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by show theme id (ex. ?show_themes=2,5)",
            ),
            OpenApiParameter(
                "title",
                type=OpenApiTypes.STR,
                description="Filter by astronomy show title "
                            "(ex. ?title=fiction)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

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


class ReservationPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 15


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.prefetch_related(
        "tickets__show_session__astronomy_show",
        "tickets__show_session__astronomy_show__planetarium_dome"
    )
    serializer_class = ReservationSerializer
    pagination_class = ReservationPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer

        return ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
