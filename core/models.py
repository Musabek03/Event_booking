from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):

    CHOICES = [("admin", "Admin"), ("client", "Client")]

    role = models.CharField(max_length=20,choices=CHOICES, default="client")
    phone_number = models.CharField(max_length=20,unique=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(upload_to='user_profile_photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ["phone_number"]


    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True,
        verbose_name="groups",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",
        blank=True,
        verbose_name="user permissions",
    )

    def __str__(self):
        return self.username
    

class Category(models.Model):

    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Event(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    image = models.ImageField(upload_to="events_images/")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f" Event: {self.title}"
    
    


class Booking(models.Model):

    CHOICES = [('kutilmekte', 'Kutilmekte'), ('tolendi', 'Tolendi'), ('biykar_etildi', 'Biykar_etildi')]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=CHOICES, default='kutilmekte')
    booking_code = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)

    def save(self,*args, **kwargs):
        if not self.total_price:
            self.total_price = self.event.price*self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"