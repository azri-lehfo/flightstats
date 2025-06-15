from datetime import date
import json

from django.test import TestCase, Client, override_settings
from django.urls import reverse

from unittest.mock import patch

# Get today's date for dynamic testing
TODAY_DATE_STR = date.today().strftime('%Y-%m-%d')


@override_settings(CELERY_ENABLED=False)
class FlightStatusAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('api:flight-service:flights-list')

    @patch('api.flights.serializers.FlightSerializer._fetch_from_api')
    def test_successful_flight_lookup(self, mock_fetch_data):
        """
        Tests that the API successfully returns flight status for a valid flight.
        Mocks the external API call to return predefined data.
        """
        # Mocked data that the external service would return for AA100
        mock_external_api_response = {
            "flightId": 1321611460,
            "flightNote": {
            "final": False,
            "canceled": False,
            "hasDepartedGate": False,
            "hasDepartedRunway": False,
            "landed": False,
            "message": "Tracking will begin after departure",
            "messageCode": "S",
            "pastExpectedTakeOff": False,
            "tracking": False,
            "hasPositions": False,
            "trackingUnavailable": False,
            "phase": None,
            "hasActualRunwayDepartureTime": False,
            "hasActualGateDepartureTime": False
            },
            "isTracking": False,
            "isLanded": False,
            "isScheduled": True,
            "sortTime": "2025-06-15T22:10:00.000Z",
            "schedule": {
            "scheduledDeparture": "2025-06-15T18:10:00.000",
            "scheduledDepartureUTC": "2025-06-15T22:10:00.000Z",
            "estimatedActualDepartureRunway": False,
            "estimatedActualDepartureTitle": "Estimated",
            "estimatedActualDeparture": "2025-06-15T18:10:00.000",
            "estimatedActualDepartureUTC": "2025-06-15T22:10:00.000Z",
            "scheduledArrival": "2025-06-16T06:20:00.000",
            "scheduledArrivalUTC": "2025-06-16T05:20:00.000Z",
            "estimatedActualArrivalRunway": False,
            "estimatedActualArrivalTitle": "Estimated",
            "estimatedActualArrival": "2025-06-16T06:20:00.000",
            "estimatedActualArrivalUTC": "2025-06-16T05:20:00.000Z",
            "graphXAxis": {
                "dep": "2025-06-15T18:10:00.000",
                "depUTC": "2025-06-15T22:10:00.000Z",
                "arr": "2025-06-16T06:20:00.000",
                "arrUTC": "2025-06-16T05:20:00.000Z"
            }
            },
            "status": {
            "statusCode": "S",
            "status": "Scheduled",
            "color": "green",
            "statusDescription": "On time",
            "delay": {
                "departure": {
                "minutes": 0
                },
                "arrival": {
                "minutes": 0
                }
            },
            "delayStatus": {
                "wording": "On time",
                "minutes": 0
            },
            "lastUpdatedText": "Status Last Updated More Than 3 Hours Ago",
            "diverted": False
            },
            "resultHeader": {
            "statusDescription": "On time",
            "carrier": {
                "name": "American Airlines",
                "fs": "AA"
            },
            "flightNumber": "100",
            "status": "Scheduled",
            "diverted": False,
            "color": "green",
            "departureAirportFS": "JFK",
            "arrivalAirportFS": "LHR",
            "divertedAirport": None
            },
            "ticketHeader": {
            "carrier": {
                "name": "American Airlines",
                "fs": "AA"
            },
            "flightNumber": "100"
            },
            "operatedBy": None,
            "departureAirport": {
            "fs": "JFK",
            "iata": "JFK",
            "name": "New York John F. Kennedy International Airport",
            "city": "New York",
            "state": "NY",
            "country": "US",
            "timeZoneRegionName": "America/New_York",
            "regionName": "North America",
            "gate": "31",
            "terminal": "8",
            "times": {
                "scheduled": {
                "time": "6:10",
                "ampm": "PM",
                "time24": "18:10",
                "timezone": "EDT"
                },
                "estimatedActual": {
                "title": "Estimated",
                "time": "6:10",
                "ampm": "PM",
                "time24": "18:10",
                "runway": False,
                "timezone": "EDT"
                }
            },
            "date": "2025-06-15T18:10:00.000"
            },
            "arrivalAirport": {
            "fs": "LHR",
            "iata": "LHR",
            "name": "London Heathrow Airport",
            "city": "London",
            "state": "EN",
            "country": "GB",
            "timeZoneRegionName": "Europe/London",
            "regionName": "Europe",
            "gate": None,
            "terminal": "3",
            "baggage": None,
            "times": {
                "scheduled": {
                "time": "6:20",
                "ampm": "AM",
                "time24": "06:20",
                "timezone": "BST"
                },
                "estimatedActual": {
                "title": "Estimated",
                "time": "6:20",
                "ampm": "AM",
                "time24": "06:20",
                "runway": False,
                "timezone": "BST"
                }
            },
            "date": "2025-06-16T06:20:00.000"
            },
            "divertedAirport": None,
            "additionalFlightInfo": {
            "equipment": {
                "iata": "77W",
                "name": "Boeing 777-300ER",
                "title": "Actual"
            },
            "flightDuration": "7h 10m"
            },
            "codeshares": [
            {
                "fs": "AS",
                "name": "Alaska Airlines",
                "flightNumber": "6904"
            },
            {
                "fs": "AY",
                "name": "Finnair",
                "flightNumber": "4012"
            },
            {
                "fs": "BA",
                "name": "British Airways",
                "flightNumber": "1511"
            },
            {
                "fs": "GF",
                "name": "Gulf Air",
                "flightNumber": "6654"
            },
            {
                "fs": "IB",
                "name": "Iberia",
                "flightNumber": "4218"
            },
            {
                "fs": "UL",
                "name": "SriLankan Airlines",
                "flightNumber": "2026"
            }
            ],
            "positional": {
            "departureAirportCode": "JFK",
            "arrivalAirportCode": "LHR",
            "divertedAirportCode": None,
            "flexFlightStatus": "S",
            "flexTrack": {
                "flightId": 1321611460,
                "carrierFsCode": "AA",
                "flightNumber": "100",
                "tailNumber": "N721AN",
                "departureAirportFsCode": "JFK",
                "arrivalAirportFsCode": "LHR",
                "departureDate": {
                "dateUtc": "2025-06-15T22:10:00.000Z",
                "dateLocal": "2025-06-15T18:10:00.000"
                },
                "equipment": "77W",
                "bearing": 51.3509835073817,
                "positions": [],
                "irregularOperations": [],
                "fleetAircraftId": 141162
            }
            },
            "flightState": "currentDatePreDeparture"
        }
        mock_fetch_data.return_value = mock_external_api_response

        # Make the request to your Django API endpoint
        response = self.client.get(
            self.url,
            {
                'airline': 'AA',
                'flight_number': '100',
                'departure_date': TODAY_DATE_STR
            },
            follow=True
        )

        # Assertions
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)

        self.assertIn('pk', response_data)
        self.assertEqual(response_data['airline_code'], 'AA')
        self.assertEqual(response_data['flight_number'], '100')
        self.assertEqual(response_data['departure_date'], TODAY_DATE_STR)
        self.assertEqual(response_data['extra_data']['resultHeader']['departureAirportFS'], 'JFK')
        self.assertEqual(response_data['extra_data']['resultHeader']['arrivalAirportFS'], 'LHR')
        self.assertEqual(response_data['extra_data']['status']['status'], 'Scheduled')
        self.assertEqual(response_data['extra_data']['resultHeader']['carrier']['name'], 'American Airlines')

        # Verify that the mock was called with the correct arguments
        mock_fetch_data.assert_called_once_with('AA', '100', TODAY_DATE_STR)


    @patch('api.flights.serializers.FlightSerializer._fetch_from_api')
    def test_flight_not_found(self, mock_fetch_data):
        """
        Tests that the API handles cases where the external service doesn't find the flight.
        """
        # Mock the external API to return an empty flightStatus (or an error indicating not found)
        mock_fetch_data.return_value = {}

        response = self.client.get(
            self.url,
            {
                'airline': 'ZZ',
                'flight_number': '99999',
                'departure_date': TODAY_DATE_STR
            },
            follow=True
        )

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn('No flight data found', response_data[0])
        mock_fetch_data.assert_called_once_with('ZZ', '99999', TODAY_DATE_STR)


    def test_missing_parameters(self):
        """
        Tests that the API returns a 400 Bad Request if required parameters are missing.
        """
        response = self.client.get(
            self.url,
            {
                'airline': 'AA',
                # 'flight_number' is missing
                'departure_date': TODAY_DATE_STR
            },
            follow=True
        )

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn('Missing required query parameters', response_data[0])

    @patch('api.flights.serializers.FlightSerializer._fetch_from_api')
    def test_external_api_error(self, mock_fetch_data):
        """
        Tests that the API handles errors from the external flight tracking service.
        """
        # Simulate an exception when calling the external service
        from requests.exceptions import RequestException
        mock_fetch_data.side_effect = RequestException("Service Unavailable")

        response = self.client.get(
            self.url,
            {
                'airline': 'AA',
                'flight_number': '100',
                'departure_date': TODAY_DATE_STR
            },
            follow=True
        )

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn('Service Unavailable', response_data[0])
        mock_fetch_data.assert_called_once_with('AA', '100', TODAY_DATE_STR)

    def test_invalid_date_format(self):
        """
        Tests that the API returns a 400 Bad Request if the date format is invalid.
        """
        response = self.client.get(
            self.url,
            {
                'airline': 'AA',
                'flight_number': '100',
                'departure_date': 'invalid-date-format'  # Invalid date format
            },
            follow=True
        )

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn('Invalid date format', response_data[0])
