import requests

from django.conf import settings

from rest_framework import serializers

from flights.models import Flight


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = (
            'pk',
            'airline_code',
            'flight_number',
            'departure_date',
            'extra_data',
        )

    def _fetch_from_api(self, airline: str, flight_number: str, departure_date: str) -> dict:
        """
        Fetch flight details from an external API.
        This method should be implemented to call the actual API and return a Flight instance.
        Store the flight data in the database if it does not exist.
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
        if response.status_code == 500:
            raise serializers.ValidationError("External API error.")
        elif response.status_code != 200:
            raise serializers.ValidationError("No flight found with the provided parameters.")

        data = response.json()
        return data

    def _get_flight_from_api(self, airline: str, flight_number: str, departure_date: str) -> Flight:
        data = self._fetch_from_api(airline, flight_number, departure_date)
        if not data:
            raise serializers.ValidationError("No flight data found.")
        flight = Flight.objects.create(
            airline_code=airline,
            flight_number=flight_number,
            departure_date=departure_date,
            extra_data=data,
        )
        return flight

    def get_flight_details(self, airline: str, flight_number: str, departure_date: str) -> Flight:
        """
        Fetch flight details based on airline, flight number, and departure date.
        This method can be overridden to implement custom logic for fetching flight details.
        """
        try:
            return Flight.objects.get(
                airline_code=airline,
                flight_number=flight_number,
                departure_date=departure_date
            )
        except Flight.DoesNotExist:
            try:
                return self._get_flight_from_api(airline, flight_number, departure_date)
            except Exception as e:
                raise serializers.ValidationError(f"An error occurred while fetching flight details: {str(e)}")
        except Flight.MultipleObjectsReturned:
            raise serializers.ValidationError("Multiple flights found with the provided parameters. Please refine your search.")
        except Exception as e:
            raise serializers.ValidationError(f"An error occurred while fetching flight details: {str(e)}")
