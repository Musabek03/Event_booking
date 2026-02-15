from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import EventsView,BookingView

router = DefaultRouter()

router.register(r"events",EventsView,basename='event')
router.register(r"bookings", BookingView, basename="booking" )

urlpatterns = [
    path("",include(router.urls))
]

