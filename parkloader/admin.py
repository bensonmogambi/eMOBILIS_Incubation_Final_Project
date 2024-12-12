from django.contrib import admin
from .models import ParkingLoader , ParkingLot,Billing,BillingPlan
# Register your models here.

admin.site.register(Billing)
admin.site.register(BillingPlan)


@admin.register(ParkingLoader)
class ParkingLoaderAdmin(admin.ModelAdmin):
    list_display = ( 'car_registration_number', 'vehicle_type','parking_lot','parked')
    fields = ( 'car_registration_number', 'vehicle_type','parking_lot', 'parked')

    def delete_model(self, request, obj):
        parking_lot = obj.parking_lot
        parking_lot.available_slots += 1  # increase available slots by 1
        parking_lot.save()  # save the updated parking lot
        obj.delete()  # delete the vehicle from the database
@admin.register(ParkingLot)
class ParkingLotAdmin(admin.ModelAdmin):
    list_display = ( 'location', 'total_slots', 'available_slots')
    fields = ( 'location', 'total_slots', 'available_slots')