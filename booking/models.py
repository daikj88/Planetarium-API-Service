import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return f"{self.name}, row: {self.rows}, seats: {self.seats_in_row}"


def astronomy_show_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/astronomy_show/", filename)


class AstronomyShow(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    show_theme = models.ManyToManyField(
        "ShowTheme",
        related_name="show_theme",
        blank=True
    )
    images = models.ImageField(null=True, upload_to=astronomy_show_image_file_path)

    def __str__(self):
        return self.title


class ShowTheme(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE)
    planetarium_dome = models.ForeignKey(PlanetariumDome, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.astronomy_show.title} {self.planetarium_dome.name} {self.show_time}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.created_at)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(
        ShowSession,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    class Meta:
        unique_together = ["seat", "show_session"]

    def __str__(self):
        return f"{self.row} {self.seat} {self.show_session}"

    @staticmethod
    def validate_seat(seat: int, num_seats: int, error_to_raise):
        if not (1 <= seat <= num_seats):
            raise error_to_raise({
                "seat": f"seat must be in range [1, {Ticket.show_session.planetarium_dome.seats_in_row}], not {seat}",
            })

    def clean(self):
        Ticket.validate_seat(self.seat, Ticket.show_session.planetarium_dome.capacity, ValueError)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )
