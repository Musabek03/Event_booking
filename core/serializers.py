from rest_framework import serializers
from .models import CustomUser,Category,Event,Booking
from rest_framework.validators import ValidationError

class EventsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['id','title', 'slug', 'description', 'location', 'date_time', 'price', 'available_seats', 'image', 'is_active']


class NestedEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['id', 'title', 'date_time']


class BookingSerializer(serializers.ModelSerializer):
    event = NestedEventSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id','user','event', 'quantity', 'status', 'booking_code', 'total_price', 'created_at' ]


class ReqeustBookingSerializer(serializers.Serializer):
    event_id  = serializers.IntegerField()
    quantity = serializers.IntegerField(default = 1, min_value = 1)


class RegisterUserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, style={'input_type':'password'}, help_text="Parol")
    confirm_password = serializers.CharField(write_only=True, required=True,style={'input_type':'password'},help_text='Paroldi tastiyqlaw')

    class Meta:
        model = CustomUser
        fields = ["username", "password", "confirm_password"]

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise ValidationError({'confirm_password':'Paroller saykes emes,qaytadan jazin!'})
        
        return attrs

    def create(self, validated_data):

        validated_data.pop('confirm_password')

        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        user.save()

        return user