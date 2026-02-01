from rest_framework import viewsets,filters, permissions,status,generics,mixins
from rest_framework.viewsets import GenericViewSet
from .models import CustomUser, Category,Event,Booking
from .serializers import EventsSerializer


class EventsView(mixins.ListModelMixin, mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer
    permission_classes = [permissions.AllowAny]

    