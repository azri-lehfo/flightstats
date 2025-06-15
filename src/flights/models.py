from django.db import models


class Flight(models.Model):
    airline_code = models.CharField(
        verbose_name="Airline code",
        max_length=10,
        db_index=True
    )
    flight_number = models.CharField(
        verbose_name="Flight number",
        max_length=10,
        db_index=True
    )
    departure_date = models.DateField(
        verbose_name="Departure date",
        db_index=True
    )
    extra_data = models.JSONField(
        verbose_name="Extra data",
        default=dict,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        verbose_name="Created at",
        auto_now=False,
        auto_now_add=True,
        db_index=True
    )
    updated_at = models.DateTimeField(
        verbose_name="Updated at",
        auto_now=True,
        auto_now_add=False,
        db_index=True
    )

    def __str__(self):
        return f"{self.airline_code} {self.flight_number} on {self.departure_date}"
