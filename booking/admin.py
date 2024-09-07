from django.contrib import admin

from booking.models import (
    ShowSession,
    PlanetariumDome,
    ShowTheme,
    AstronomyShow,
    Reservation,
    Ticket
)

admin.site.register(ShowSession)
admin.site.register(ShowTheme)
admin.site.register(AstronomyShow)
admin.site.register(Reservation)
admin.site.register(Ticket)
admin.site.register(PlanetariumDome)
