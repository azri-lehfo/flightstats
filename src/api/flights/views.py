from datetime import datetime

from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from flights.models import Flight

from ..cache import CacheModelViewSetMixin
from .serializers import FlightSerializer


class FlightViewSet(CacheModelViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet for fetching flight data.
    It inherits from CacheModelViewSetMixin to enable caching functionality.
    This API use GET parameters to filter flights by airline, flight number, and date.
    The API endpoint is `/api/flights-service/flights/`.
    The paramseters are:
    - `airline`: The airline code (e.g., 'AA' for American Airlines).
    - `flight_number`: The flight number (e.g., '123').
    - `departure_date`: The date of departure in the format 'YYYY-MM-DD' (e.g., '2023-10-01').
    The serializer used is `FlightSerializer`, which defines the fields to be serialized.
    The queryset is set to retrieve all Flight objects from the database if any.
    """
    allowed_methods = ['GET']  # Only allow GET requests for this viewset
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()
    cache_key_prefix = 'flight'

    def list(self, request, *args, **kwargs):
        """
        Handle query parameters to fetch flight information.
        """
        airline = request.query_params.get('airline')
        flight_number = request.query_params.get('flight_number')
        departure_date = request.query_params.get('departure_date')

        if not all([airline, flight_number, departure_date]):
            raise ValidationError("Missing required query parameters: airline, flight_number, and departure_date are all required.")

        try:
            datetime.strptime(departure_date, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Invalid date format for departure_date. Use 'YYYY-MM-DD'.")

        # Get flight details from API or database
        flight = self.serializer_class().get_flight_details(
            airline=airline,
            flight_number=flight_number,
            departure_date=departure_date
        )
        if not flight:
            raise ValidationError("Flight not found with the provided parameters.")
        # Use the retrieve method to return the flight details
        # Cache will be handled by the mixin
        return self.retrieve(pk=flight.pk, instance=flight, request=request, *args, **kwargs)
