from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.models import User




# BillingPlan model for parking plans
class BillingPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    max_bookings = models.IntegerField()

    def __str__(self):
        return self.name

# Billing model for storing user billing information
class Billing(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(BillingPlan, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=20)
    #card_expiry = models.CharField(max_length=10)
    #cvv = models.CharField(max_length=5)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.plan = None

    def __str__(self):
        return f'{self.user.username} ({self.plan.name})'


# Vehicle model for car registrations
class Vehicle(models.Model):
    name = models.CharField(max_length=100, default="name")
    license_plate = models.CharField(max_length=20, default='KCL 545')
    time_in = models.DateTimeField(default=now)
    expected_time_out = models.DateTimeField(default=now)
    phone_number = models.CharField(max_length=15, default='0759194307')
    color = models.CharField(max_length=50, default='e.g., black')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    VEHICLE_TYPE_CHOICES = [
        ('lorry', 'Lorry'),
        ('van', 'Van'),
        ('matatu', 'Matatu'),
        ('personal', 'Personal')
    ]
    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPE_CHOICES,
        default='car',
    )
    car_registration_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.car_registration_number} - {self.vehicle_type}"




"""""

class ParkingLot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    location = models.CharField(max_length=255)
    total_slots = models.IntegerField()
    available_slots = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.pk:  # Initialize available slots for new parking lots
            self.available_slots = self.total_slots
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.location} ({self.available_slots}/{self.total_slots} slots available)"
"""



# ParkingLoader model to track vehicle parking status
class ParkingLoader(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Billing, on_delete=models.CASCADE, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)  # Linked to Vehicle model
    time_in = models.DateTimeField(auto_now_add=True)
    parked = models.BooleanField(default=True)
    vehicle_type = models.CharField(max_length=100)
    car_registration_number = models.CharField(max_length=100, default="UNKNOWN")

    def __str__(self):
        return f"{self.vehicle.car_registration_number} - Parked: {self.parked}"






# ParkingSpace model to represent various parking locations
class ParkingSpace(models.Model):

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    pin = models.CharField(max_length=400, default=" pin your location")
    phone_number = models.CharField(max_length=20)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    facility_type = models.CharField(
        max_length=100,
        choices=[('university', 'University'), ('church', 'Church'), ('highschool', 'High School'), ('other', 'Other')]
    )
    photo = models.ImageField(upload_to='parking_photos/', null=True, blank=True)

    def __str__(self):
        return self.name






# Booking model to track vehicle bookings for parking spaces

class VehicleBooking(models.Model):
    # Vehicle Details
    car_registration_number = models.CharField(max_length=100, unique=True)
    vehicle_type = models.CharField(
        max_length=20,
        choices=[
            ('lorry', 'Lorry'),
            ('van', 'Van'),
            ('matatu', 'Matatu'),
            ('personal', 'Personal')
        ],
        default='personal',
    )
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    color = models.CharField(max_length=50)

    # Booking Details
    time_in = models.DateTimeField(default=now)
    expected_time_out = models.DateTimeField()


    # Relations
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Booking for {self.car_registration_number} at {self.time_in}"