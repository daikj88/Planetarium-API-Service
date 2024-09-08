from django.contrib import admin

from booking.models import (
    ShowSession,
    PlanetariumDome,
    ShowTheme,
    AstronomyShow,
    Reservation,
    Ticket
)


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


class ReservationAdmin(admin.ModelAdmin):
    inlines = [TicketInLine]


admin.site.register(ShowSession)
admin.site.register(ShowTheme)
admin.site.register(AstronomyShow)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Ticket)
admin.site.register(PlanetariumDome)
