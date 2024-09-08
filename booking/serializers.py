from rest_framework import serializers

from booking.models import (
    AstronomyShow,
    PlanetariumDome,
    ShowTheme,
    ShowSession,
    Ticket,
    Reservation
)


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "show_theme")


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class ShowSessionSerializer(serializers.ModelSerializer):
    planetarium_dome = PlanetariumDomeSerializer(many=False, read_only=True)
    astronomy_show = PlanetariumDomeSerializer(many=False, read_only=True)

    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user")


class TicketSerializer(serializers.ModelSerializer):
    show_sessions = ShowSessionSerializer(many=False, read_only=True)
    reservations = ReservationSerializer(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session", "reservation")

    def validate(self, attrs):
        Ticket.validate_seat(
            attrs["seat"],
            attrs["show_session"].planetarium_dome.seats_in_row,
            serializers.ValidationError,
        )
