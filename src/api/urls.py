from django.urls import path, include


app_name = 'api'

urlpatterns = [
    path(
        'flight-service/',include('api.flights.urls', namespace='flight-service')
    ),
]
