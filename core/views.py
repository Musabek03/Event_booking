from rest_framework import viewsets,filters, permissions,status,generics,mixins
from rest_framework.viewsets import GenericViewSet
from .models import CustomUser, Category,Event,Booking
from .serializers import EventsSerializer,BookingSerializer,ReqeustBookingSerializer, RegisterUserSerializer
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

class EventsView(mixins.ListModelMixin, mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer
    permission_classes = [permissions.AllowAny]


class BookingView(GenericViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    @extend_schema(request=None, responses={204:None})
    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        booking = get_object_or_404(Booking, pk=pk, user=request.user)
        with transaction.atomic():
            event = booking.event
            event.available_seats += booking.quantity
            event.save()

            booking.delete()

        return Response({'message':'Bron biykar etildi'},status=status.HTTP_204_NO_CONTENT)

    
    
    @action(detail=False, methods=['get'])
    def my_tickets(self,request):
        bookings = Booking.objects.filter(user=self.request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)
        



    @extend_schema(request=ReqeustBookingSerializer)
    @action(detail=False, methods=['post'])
    def book_event(self,request):
        serializer = ReqeustBookingSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        event_id = serializer.validated_data['event_id']
        quantity = serializer.validated_data['quantity']

        event  = get_object_or_404(Event, id=event_id)

        booking, created = Booking.objects.get_or_create(user=self.request.user, event=event,  defaults={'quantity': quantity})

        new_quantity = quantity if created else booking.quantity + quantity

        if event.date_time < timezone.now():
            raise ValidationError({"detail": "Otip ketken eventke bilet alip bolmaydi"})

        if new_quantity > 5:
            return Response({'error':'Bir user maksimum 5 bilet bronlawi mumkin!'}, status=status.HTTP_400_BAD_REQUEST)

        if not event.is_active:
            return Response({'error':'Aktiv emes event'}, status=status.HTTP_400_BAD_REQUEST)

        if event.available_seats < quantity:
            return Response({'error': f'Eventte bunsha bos orin joq, qalgan biletler sani: {event.available_seats} '}, status=status.HTTP_400_BAD_REQUEST)
        
        if not event.available_seats - new_quantity > 0:
            return Response({'error':f'Bul mugdarda bilet qalmagan, qalgan biletler sani: {event.available_seats}'}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            event.available_seats -= quantity
            event.save()

            booking.quantity = new_quantity
            booking.total_price = booking.event.price * new_quantity
            booking.save()


        return Response({'success': 'Bilet bronlandi'})


class UsereRegisterView(generics.CreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer



    

