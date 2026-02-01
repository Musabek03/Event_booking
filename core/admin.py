from django.contrib import admin
from .models import Event,Category


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'slug', 'description', 'location', 'date_time', 'price', 'available_seats', 'image', 'is_active')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')