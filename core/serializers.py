from rest_framework import serializers
from .models import CustomUser,Category,Event,Booking


class EventsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['id','title', 'slug', 'description', 'location', 'date_time', 'price', 'available_seats', 'image', 'is_active']
    

class BookingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booking
        fields = ['id','user', 'quantity', 'status', 'booking_code', 'total_price', 'created_at' ]
    
class ReqeustBookingSerializer(serializers.Serializer):
    event_id  = serializers.IntegerField()
    quantity = serializers.IntegerField(default = 1, min_value = 1)