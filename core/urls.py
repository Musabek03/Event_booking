from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import EventsView,BookingView, UsereRegisterView, AdminDashboardView, CategoryViewSet

router = DefaultRouter()

router.register(r"events",EventsView,basename='event')
router.register(r"bookings", BookingView, basename="booking" )
router.register(r"category", CategoryViewSet, basename="category")

urlpatterns = [
    path("",include(router.urls)),
    path("register", UsereRegisterView.as_view(), name="register"),
    path("dashboard",AdminDashboardView.as_view(), name="dashboard")
]

