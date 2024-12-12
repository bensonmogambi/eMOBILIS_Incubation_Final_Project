
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django_daraja.mpesa.core import MpesaClient
from .models import ParkingLot, Billing, BillingPlan, VehicleBooking
from .forms import LoginForm, RegisterForm, BillingForm, ParkingSpaceRegistrationForm,  VehicleBookingForm
from .forms import   BillingForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import logging
logger = logging.getLogger(__name__)




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
    parking_lots = ParkingLot.objects.all()
    parking_lot_choices = [(lot.id, f"{lot.location} ({lot.available_slots} available)") for lot in parking_lots]

    vehicle_booking_form = VehicleBookingForm(user=request.user)
    parking_space_form = ParkingSpaceRegistrationForm()

    return render(request, 'home.html', {
        'vehicle_booking_form': vehicle_booking_form,
        'parking_space_form': parking_space_form,
        'parking_lot_choices': parking_lot_choices
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
def billing(request):
    plans = BillingPlan.objects.all()
    user = request.user
    billing, created = Billing.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = BillingForm(request.POST, instance=billing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Billing details successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Billing plan not selected!')
            return redirect('login')
    else:
        form = BillingForm(instance=billing)
        return render(request, 'billingplans.html', {'plans': plans, 'form': form})

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
    data = request.body
    return HttpResponse("STK Push in Django👋")
