from django.contrib import admin
from .models import Event,Category, Booking, CustomUser
from django.contrib.auth.admin import UserAdmin

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'slug', 'description', 'location', 'date_time', 'price', 'available_seats', 'image', 'is_active')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'quantity', 'status', 'booking_code', 'created_at', 'updated_at', 'total_price' )


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
     list_display = ('username', 'first_name', 'last_name', 'phone_number',  'is_staff')