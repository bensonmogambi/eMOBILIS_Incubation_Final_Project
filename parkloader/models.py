from django.db import models
from django.contrib.auth.models import User
# Create your models here.


#create tople for the vehicle drop downs 
vehicle_type_choice = (('lorry','lorry'),('large vehicle','large vehicle') , ('pickup','pickup'),('personal car','personal car'))


# create parking lot models which will be tables after sqlmigrate 

class ParkingLot(models.Model):
    location = models.CharField(max_length=100)
    total_slots = models.IntegerField()
    available_slots = models.IntegerField()

    def save(self, *args, **kwargs):
        # Initialize available_slots to total_slots when a new parking lot is created
        if not self.pk:
            self.available_slots = self.total_slots
        super(ParkingLot, self).save(*args, **kwargs)

    def __str__(self):
        return self.location


class Billing(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey('BillingPlan', on_delete=models.CASCADE, null=True)
    card_number = models.CharField(max_length=20)
    card_expiry = models.CharField(max_length=10)
    cvv = models.CharField(max_length=5)

    def __str__(self):
        return f'{self.user.username} ({self.plan})'
    

class parkingLoader(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Billing, on_delete=models.CASCADE,null=True)
    car_regestration_number= models.CharField(max_length = 8)
    vehicle_type = models.TextField(max_length = 50,choices= vehicle_type_choice)
    time_in = models.DateTimeField(auto_now_add = True)
    parked = models.BooleanField(default=True)
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE,null=True)


    def __str__(self):
        return self.car_regestration_number
    
class BillingPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    max_bookings = models.IntegerField()
    
    def __str__(self):
        return self.name