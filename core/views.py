from rest_framework import viewsets,filters, permissions,status,generics,mixins
from rest_framework.viewsets import GenericViewSet
from .models import CustomUser, Category,Event,Booking
from .serializers import EventsSerializer,BookingSerializer


class EventsView(mixins.ListModelMixin, mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer
    permission_classes = [permissions.AllowAny]



class BookingView(mixins.ListModelMixin, mixins.DestroyModelMixin,GenericViewSet):
    queryset = Booking
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]

