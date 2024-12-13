
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django_daraja.mpesa.core import MpesaClient
from .models import  Billing, BillingPlan, VehicleBooking, ParkingSpace
from .forms import LoginForm, RegisterForm, BillingForm, ParkingSpaceRegistrationForm, VehicleBookingForm, \
    MpesaPaymentForm
from .forms import   BillingForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import logging
logger = logging.getLogger(__name__)
from .mpesa_client import MpesaClient  # Ensure you have MpesaClient class to handle the Mpesa integration
from rest_framework.views import APIView
from rest_framework import status
import json
from django.http import JsonResponse






def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            user_plan = Billing.objects.filter(user=user).first()
            return redirect("home" if user_plan else 'billing_info2')
        else:
            return render(request, 'login.html', {'form': form, 'error_message': ""})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form, 'error_message': ""})





# Home view for booking and registering parking spots
@login_required(login_url='/login/')
def home(request):


    vehicle_booking_form = VehicleBookingForm(user=request.user)
    parking_space_form = ParkingSpaceRegistrationForm()

    return render(request, 'home.html', {
        'vehicle_booking_form': vehicle_booking_form,
        'parking_space_form': parking_space_form,

    })








@login_required(login_url='/login/')
def book_parking(request):
    if request.method == 'POST':
        logger.info(f"POST data: {request.POST}")
        vehicle_booking_form = VehicleBookingForm(request.POST, user=request.user)

        if vehicle_booking_form.is_valid():
            vehicle_booking_form.save()
            messages.success(request, 'Your booking has been successful!')
            return redirect(reverse('home') + '#book')
        else:
            logger.error(f"Form errors: {vehicle_booking_form.errors}")
            messages.error(request, 'An error occurred while processing your booking.')

    vehicle_booking_form = VehicleBookingForm(user=request.user)
    parking_spaces = ParkingSpace.objects.all()
    return render(request, 'home.html', {
            'vehicle_booking_form': vehicle_booking_form,
            'parking_spaces': parking_spaces  }) # Display parking spaces


@login_required(login_url='/login/')
def view_bookings(request):
    # Fetch all bookings for the logged-in user
    bookings = VehicleBooking.objects.filter(parking_lot__user=request.user)
    return render(request, 'view_bookings.html', {'bookings': bookings})



def cancel_booking(request, booking_id):
    # Get the booking object
    booking = get_object_or_404(VehicleBooking, id=booking_id)

    # Ensure only the user who created the booking can cancel it
    if booking.vehicle.user != request.user:
        messages.error(request, "You are not authorized to cancel this booking.")
        return HttpResponseRedirect(reverse('view_bookings'))

    # Release the parking lot slot
    parking_lot = booking.parking_lot
    parking_lot.available_slots += 1
    parking_lot.save()

    # Delete the booking
    booking.delete()
    messages.success(request, "Booking has been successfully canceled.")
    return HttpResponseRedirect(reverse('view_bookings'))







@login_required(login_url='/login/')
def register_parking_spot(request):
    if request.method == 'POST':
        parking_space_form = ParkingSpaceRegistrationForm(request.POST, request.FILES)
        if parking_space_form.is_valid():
            parking_space = parking_space_form.save(commit=False)
            parking_space.user = request.user  # Ensure the parking space is linked to the logged-in user, if applicable
            parking_space.save()
            messages.success(request, 'Your parking spot has been successfully registered!')
            return redirect(reverse('home') + '#register')
        else:
            # Debug: Log the form errors
            print("Form errors:", parking_space_form.errors)  # For debugging in the console
            messages.error(request, 'An error occurred while registering your parking spot.')
    else:
        parking_space_form = ParkingSpaceRegistrationForm()

    return render(request, 'home.html', {'parking_space_form': parking_space_form})




# Registration form view
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login")
        else:
            return render(request, 'signUp.html', {'form': form, 'error_message': "Invalid username or password."})
    else:
        form = RegisterForm()
        return render(request, 'signUp.html', {'form': form})



# Billing information view
def billing_info(request):
    billing_plans = BillingPlan.objects.all()
    return render(request, 'billing.html', {'billing_plans': billing_plans})





# Billing view
@login_required
def billing(request):
    user = request.user
    plans = BillingPlan.objects.all()
    billing, created = Billing.objects.get_or_create(user=user, defaults={'plan': None, 'phone_number': ''})

    if request.method == 'POST':
        form = MpesaPaymentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone_number = form.cleaned_data['phone_number']
            selected_plan = form.cleaned_data['plan']
            amount = selected_plan.price  # Get the price from the selected plan

            # Mpesa STK push
            try:
                cl = MpesaClient()
                account_reference = f"Plan-{selected_plan.name}"
                transaction_desc = f"Payment for {selected_plan.name}"
                callback_url = 'http://127.0.0.1:8000/mpesa/callback/'

                response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
                if response.get('ResponseCode') == '0':
                    billing.plan = selected_plan
                    billing.phone_number = phone_number
                    billing.save()

                    messages.success(request, 'Payment request sent. Check your phone to complete the transaction.')
                    return redirect('home')
                else:
                    messages.error(request, 'Failed to initiate payment. Please try again.')
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
        else:
            messages.error(request, 'Invalid payment details entered.')
    else:
        form = MpesaPaymentForm()

    return render(request, 'billingplans.html', {'form': form, 'plans': plans, 'billing': billing})







# STK push view (mpesa payment)
def index(request):
    cl = MpesaClient()
    phone_number = '0759194307'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://darajambili.herokuapp.com/express-payment'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)

# STK push callback

def stk_push_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse callback data
        print(f"Mpesa Callback Data: {data}")
        # Process callback data here (e.g., update database, verify payment)
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})  # Send acknowledgment
    return JsonResponse({"ResultCode": 1, "ResultDesc": "Rejected"})


def mpesa_payment_callback(request):
    data = request.body
    # You can process the response here based on the status of the payment
    print(f"Callback Data: {data}")
    # Depending on the callback, you can store the result in the database or take appropriate actions

    return HttpResponse("STK Push callback received")






















"""""

# Update VehicleBooking
def update_booking(request, booking_id):
    booking = get_object_or_404(VehicleBooking, id=booking_id)
    if request.method == 'POST':
        form = VehicleBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('view_bookings')  # Redirect to the bookings list
    else:
        form = VehicleBookingForm(instance=booking)
    return render(request, 'db.html', {'form': form})


# Delete VehicleBooking
def delete_booking(request, booking_id):
    booking = get_object_or_404(VehicleBooking, id=booking_id)
    if request.method == 'POST':
        booking.delete()
        return redirect('view_bookings')  # Redirect to the bookings list
    return render(request, 'db.html', {'booking': booking})


# Update ParkingSpace
def update_parking_space(request, parking_space_id):
    parking_space = get_object_or_404(ParkingSpace, id=parking_space_id)
    if request.method == 'POST':
        form = ParkingSpaceRegistrationForm(request.POST, instance=parking_space)
        if form.is_valid():
            form.save()
            return redirect('view_parking_spaces')  # Redirect to the parking spaces list
    else:
        form = ParkingSpaceRegistrationForm(instance=parking_space)
    return render(request, 'db.html', {'form': form})


# Delete ParkingSpace
def delete_parking_space(request, parking_space_id):
    parking_space = get_object_or_404(ParkingSpace, id=parking_space_id)
    if request.method == 'POST':
        parking_space.delete()
        return redirect('view_parking_spaces')  # Redirect to the parking spaces list
    return render(request, 'db.html', {'parking_space': parking_space})






def access_db(request):
    bookings = VehicleBooking.objects.all()
    parking_spaces = ParkingSpace.objects.all()

    context = {
        'bookings': bookings,
        'parking_spaces': parking_spaces,
    }
    return render(request, 'db.html', context)
"""


