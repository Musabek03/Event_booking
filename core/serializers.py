from rest_framework import serializers
from .models import CustomUser,Category,Event,Booking


class EventsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['id','title', 'slug', 'description', 'location', 'date_time', 'price', 'available_seats', 'image', 'is_active']
        