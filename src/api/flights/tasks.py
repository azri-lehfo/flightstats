import requests

from django.conf import settings

from celery import shared_task
from rest_framework import serializers


@shared_task(name='flights.get_flight_details')
def get_flight_details(airline: str, flight_number: str, departure_date: str) -> dict:
    """
    Task to fetch flight details from an external API.
    """
    url = settings.API_URL
    if not url:
        raise serializers.ValidationError("Flight API URL is not configured in settings.")

    year = departure_date.split('-')[0]
    month = departure_date.split('-')[1]
    day = departure_date.split('-')[2]

    response = requests.get(
        url.format(
            airline=airline,
            flight_number=flight_number,
            year=year,
            month=month,
            day=day
        ),
        timeout=10,
    )
    return {
        "status_code": response.status_code,
        "data": response.json()
    }
