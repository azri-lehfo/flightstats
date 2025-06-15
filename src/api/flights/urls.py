from rest_framework import routers

from . import views


app_name = 'api.flights'

router = routers.DefaultRouter()
router.register(r'flights', views.FlightViewSet, 'flights')

urlpatterns = router.urls
