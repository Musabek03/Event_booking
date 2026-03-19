from rest_framework import viewsets,filters, permissions,status,generics,mixins
from rest_framework.viewsets import GenericViewSet
from .models import CustomUser, Category,Event,Booking, Waitlist
from .serializers import EventsSerializer,BookingSerializer,RequestBookingSerializer, RegisterUserSerializer, CategorySerializer
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrReadOnly
from django.db.models import Sum,Count
from rest_framework.views import APIView

class EventsView(mixins.ListModelMixin, mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category', 'date_time'] 
    search_fields = ['title', 'location']
    ordering_fields = ['title', 'price', 'date_time']

    @extend_schema(request=None )
    @action(detail=True, methods=['post'],permission_classes=[permissions.IsAuthenticated])
    def waitlist(self, request, pk=None):
        event = get_object_or_404(Event, pk=pk)
        
        if event.available_seats>0:
            return Response({'xabar': 'Biletler bar , satip alaberin!'})
        if Waitlist.objects.filter(user = request.user, event=event).exists():
            return Response({'xabar': 'Siz kutiw diziminde barsiz'})
        
        Waitlist.objects.create(user=request.user, event=event)

        return Response({'success': 'Kútiw dizimine tabıslı qosıldıńız!'})  

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

        first_waiting = Waitlist.objects.filter(event=event).order_by('created_at').first()

        if first_waiting: 
            print(f"XABARNAMA: Húrmetli {first_waiting.user.username}, {event.title} ilajına orın bosadı!")
            first_waiting.delete()

        return Response({'message':'Bron biykar etildi'},status=status.HTTP_204_NO_CONTENT)

    
    
    @action(detail=False, methods=['get'])
    def my_tickets(self,request):
        bookings = Booking.objects.filter(user=self.request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)
        



    @extend_schema(request=RequestBookingSerializer)
    @action(detail=False, methods=['post'])
    def book_event(self,request):
        serializer = RequestBookingSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        event_id = serializer.validated_data['event_id']
        quantity = serializer.validated_data['quantity']

        with transaction.atomic():
            event  = Event.objects.select_for_update().get(id=event_id)

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
            
        
            event.available_seats -= quantity
            event.save()

            booking.quantity = new_quantity
            booking.save()


        return Response({'success': 'Bilet bronlandi'})


class UsereRegisterView(generics.CreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer


class AdminDashboardView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self,request):
        revenue_data = Booking.objects.filter(status='tolendi').aggregate(total=Sum('total_price'))
        total_revenue = revenue_data['total'] or 0

        top_event_data = Booking.objects.values('event__title').annotate(total_sold=Sum('quantity')).order_by('-total_sold').first()
        top_event = top_event_data if top_event_data else "Ele bilet Satilmadi"

        tickets_data = Booking.objects.aggregate(total_tct=Sum('quantity'))
        total_tickets = tickets_data['total_tct'] or 0
    
        return Response({
            'total_revenue': total_revenue,
            'top_event': top_event,
            'total_tickets': total_tickets
        })


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    

