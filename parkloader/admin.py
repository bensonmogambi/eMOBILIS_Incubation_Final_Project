
from django.contrib import admin
from .models import ParkingLoader, Billing, BillingPlan, ParkingSpace, Vehicle, VehicleBooking
from django.utils.html import mark_safe

# Register Billing and BillingPlan models
admin.site.register(Billing)
admin.site.register(BillingPlan)
admin.site.register(VehicleBooking)

# ParkingLoader Admin
@admin.register(ParkingLoader)
class ParkingLoaderAdmin(admin.ModelAdmin):
    list_display = ('car_registration_number', 'vehicle_type',  'parked', 'time_in', 'user')
    fields = ('car_registration_number', 'vehicle_type',  'time_in', 'parked', 'user')

    def delete_model(self, request, obj):
        parking_lot = obj.parking_lot
        parking_lot.available_slots += 1  # increase available slots by 1
        parking_lot.save()  # save the updated parking lot
        obj.delete()  # delete the vehicle from the database




# ParkingSpace Admin
@admin.register(ParkingSpace)
class ParkingSpaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'phone_number', 'facility_type', 'photo_display')
    fields = ('name', 'location', 'pin', 'phone_number', 'opening_time', 'closing_time', 'facility_type', 'photo')
    readonly_fields = ('photo_display',)

    def photo_display(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100" height="100" />')
        return "No photo"
    photo_display.short_description = 'Photo'

# Vehicle Admin (optional)
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('car_registration_number', 'vehicle_type', 'name', 'license_plate', 'user')
    fields = ('car_registration_number', 'vehicle_type', 'name', 'license_plate', 'user', 'time_in', 'expected_time_out', 'phone_number', 'color')

    def save_model(self, request, obj, form, change):
        if not change:  # Only set the user if it's a new vehicle
            obj.user = request.user
        super().save_model(request, obj, form, change)
















"""""
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


"""