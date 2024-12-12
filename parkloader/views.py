
"""""

from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django_daraja.mpesa.core import MpesaClient
from .models import ParkingLot, Billing, BillingPlan
from .forms import MyForm, ParkingLotForm, BillingForm

# User login view
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

    if request.method == 'POST':
        if 'book_parking' in request.POST:
            vehicle_form = MyForm(request.POST)
            if vehicle_form.is_valid():
                parking_lot = ParkingLot.objects.get(id=request.POST.get('parking_lot'))
                if parking_lot.available_slots > 0:
                    vehicle = vehicle_form.save(commit=False)
                    vehicle.user = request.user
                    vehicle.parking_lot = parking_lot
                    vehicle.save()
                    parking_lot.available_slots -= 1
                    parking_lot.save()
                    messages.success(request, 'Your booking has been successfully submitted!')
                    return redirect(reverse('home') + '#book')
                else:
                    vehicle_form.add_error('parking_lot', 'No available parking slots.')
            else:
                messages.error(request, 'An error occurred while processing your booking.')
        elif 'register_parking' in request.POST:
            parking_lot_form = ParkingLotForm(request.POST)
            if parking_lot_form.is_valid():
                parking_lot = parking_lot_form.save(commit=False)
                parking_lot.owner = request.user
                parking_lot.save()
                messages.success(request, 'Your parking spot has been successfully registered!')
                return redirect(reverse('home') + '#register')
            else:
                messages.error(request, 'An error occurred while registering your parking spot.')
    else:
        vehicle_form = MyForm(user=request.user)
        parking_lot_form = ParkingLotForm()

    return render(request, 'home.html', {
        'vehicle_form': vehicle_form,
        'parking_lot_form': parking_lot_form,
        'parking_lot_choices': parking_lot_choices
    })

# Registration form view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login")
        else:
            return render(request, 'signUp.html', {'form': form, 'error_message': "Invalid username or password."})
    else:
        form = UserCreationForm()
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


"""""

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django_daraja.mpesa.core import MpesaClient
from .models import ParkingLot, Billing, BillingPlan, Vehicle
from .forms import LoginForm, RegisterForm, BillingForm, VehicleForm, BookingForm, ParkingSpaceRegistrationForm
from .forms import   BillingForm



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

    vehicle_form = VehicleForm(user=request.user)
    parking_lot_form = ParkingSpaceRegistrationForm()

    return render(request, 'home.html', {
        'vehicle_form': vehicle_form,
        'parking_lot_form': parking_lot_form,
        'parking_lot_choices': parking_lot_choices
    })


@login_required(login_url='/login/')
def book_parking(request):
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)

        if booking_form.is_valid():
            booking_form.save()
            messages.success(request, 'Your booking has been successfully submitted!')
            return redirect(reverse('home') + '#book')
        else:
            messages.error(request, 'An error occurred while processing your booking.')
    else:
        booking_form = BookingForm()

    return render(request, 'home.html', {
        'booking_form': booking_form
    })


"""""
@login_required(login_url='/login/')
def book_parking(request):
    if request.method == 'POST':
        #vehicle_form = VehicleForm(request.POST, user=request.user)
        booking_form = BookingForm(request.POST)
       # if vehicle_form.is_valid() and booking_form.is_valid():
        if booking_form.is_valid():
            parking_lot = ParkingLot.objects.get(id=request.POST.get('parking_lot'))
            if parking_lot.available_slots > 0:
                # Save vehicle instance
                vehicle = vehicle_form.save(commit=False)
                vehicle.user = request.user
                vehicle.parking_lot = parking_lot
                vehicle.save()

                # Save booking instance
                booking = booking_form.save(commit=False)
                booking.vehicle = vehicle  # Link vehicle to the booking
                booking.parking_lot = parking_lot
                booking.save()

                # Update parking lot availability
                parking_lot.available_slots -= 1
                parking_lot.save()

                messages.success(request, 'Your booking has been successfully submitted!')
                return redirect(reverse('home') + '#book')
            else:
                vehicle_form.add_error('parking_lot', 'No available parking slots.')
        else:
            messages.error(request, 'An error occurred while processing your booking.')
    else:
        vehicle_form = VehicleForm(user=request.user)
        booking_form = BookingForm()

    return render(request, 'home.html', {'vehicle_form': vehicle_form, 'booking_form': booking_form})
"""


@login_required(login_url='/login/')
def register_parking_spot(request):
    if request.method == 'POST':
        parking_lot_form = ParkingSpaceRegistrationForm(request.POST)
        if parking_lot_form.is_valid():
            parking_lot = parking_lot_form.save(commit=False)
            parking_lot.user = request.user
            parking_lot.save()
            messages.success(request, 'Your parking spot has been successfully registered!')
            return redirect(reverse('home') + '#register')
        else:
            messages.error(request, 'An error occurred while registering your parking spot.')
    else:
        parking_lot_form = ParkingSpaceRegistrationForm()

    return redirect(reverse('home'))






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
