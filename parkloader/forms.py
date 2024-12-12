from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from .models import ParkingLoader, ParkingLot, Billing, Vehicle, Booking, ParkingSpace



class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Please enter a correct %(username)s and password. Note that both fields may be case-sensitive.",
        'inactive': "This account is inactive.",
    }

    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            elif not user.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
        return self.cleaned_data



class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = Layout(
            Field('username', placeholder='Username', autofocus=''),
            Field('email', placeholder='Email'),
            Field('password1', placeholder='Password'),
            Field('password2', placeholder='Password Confirmation'),
        )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        if not username.isalnum():
            raise forms.ValidationError("Username should only contain letters and numbers.")
        return username




class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['plan', 'card_number', 'card_expiry', 'cvv']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('plan', css_class='form-group col-md-6 mb-0'),
                Column('card_number', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('card_expiry', css_class='form-group col-md-6 mb-0'),
                Column('cvv', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Field('submit', type='submit', value='Submit', css_class='btn btn-primary')
        )




class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'license_plate', 'vehicle_type', 'parking_lot']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user argument
        super(VehicleForm, self).__init__(*args, **kwargs)
        if user:
            self.user = user
            # Example: Filter parking_lot choices based on the user
            if 'parking_lot' in self.fields:
                self.fields['parking_lot'].queryset = ParkingLot.objects.filter(user=self.user)



class BookingForm(forms.ModelForm):
    # Add vehicle-related fields to the form explicitly
    car_registration_number = forms.CharField(max_length=100, required=True, label="Car Registration Number")
    vehicle_type = forms.ChoiceField(choices=Vehicle.VEHICLE_TYPE_CHOICES, required=True, label="Vehicle Type")

    class Meta:
        model = Booking
        fields = ['time_in', 'expected_time_out', 'phone_number', 'color', 'parking_lot']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the vehicle fields dynamically from the selected vehicle instance
        if self.instance and self.instance.vehicle:
            self.fields['car_registration_number'].initial = self.instance.vehicle.car_registration_number
            self.fields['vehicle_type'].initial = self.instance.vehicle.vehicle_type

    def save(self, commit=True):
        # Save the booking instance
        booking = super().save(commit=False)
        # Update or create the associated vehicle
        if self.cleaned_data.get('car_registration_number') and self.cleaned_data.get('vehicle_type'):
            vehicle, _ = Vehicle.objects.get_or_create(
                car_registration_number=self.cleaned_data['car_registration_number'],
                defaults={'vehicle_type': self.cleaned_data['vehicle_type']}
            )
            booking.vehicle = vehicle
        if commit:
            booking.save()
        return booking




"""""
class BookingForm(forms.ModelForm):
    # Add vehicle-related fields to the form explicitly
    car_registration_number = forms.CharField(max_length=100, required=True)
    vehicle_type = forms.ChoiceField(choices=Vehicle.VEHICLE_TYPE_CHOICES, required=True)

    class Meta:
        model = Booking
        fields = [ 'time_in', 'expected_time_out', 'phone_number', 'color', 'parking_lot']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the vehicle fields dynamically from the selected vehicle instance
        if self.instance and self.instance.vehicle:
            self.fields['car_registration_number'].initial = self.instance.vehicle.car_registration_number
            self.fields['vehicle_type'].initial = self.instance.vehicle.vehicle_type


"""""



class ParkingSpaceRegistrationForm(forms.ModelForm):
    class Meta:
        model = ParkingSpace
        fields = [
            'name',
            'location',
            'pin',
            'phone_number',
            'opening_time',
            'closing_time',
            'facility_type',
            'photo'
        ]















"""""
# Parking Loader Form
class ParkingLoaderForm(forms.ModelForm):
    parking_lot = forms.ModelChoiceField(queryset=ParkingLot.objects.all(), label="Parking Lot")

    class Meta:
        model = ParkingLoader
        fields = ["car_registration_number", "vehicle_type"]
        labels = {
            'car_registration_number': "Car Registration Number",  # Corrected spelling here
            'vehicle_type': "Vehicle Type",
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get user from kwargs
        super().__init__(*args, **kwargs)


# Parking Lot Form
class ParkingLotForm(forms.ModelForm):
    class Meta:
        model = ParkingLot
        fields = ['location']
        labels = {'location': 'Parking Lot Location'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('location', css_class='form-control')
        )


# Login Form
class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Please enter a correct %(username)s and password. Note that both fields may be case-sensitive.",
        'inactive': "This account is inactive.",
    }

    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            elif not user.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
        return self.cleaned_data


# Registration Form
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = Layout(
            Field('username', placeholder='Username', autofocus=''),
            Field('email', placeholder='Email'),
            Field('password1', placeholder='Password'),
            Field('password2', placeholder='Password Confirmation'),
        )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        if not username.isalnum():
            raise forms.ValidationError("Username should only contain letters and numbers.")
        return username


# Billing Form
class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['plan', 'card_number', 'card_expiry', 'cvv']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('plan', css_class='form-group col-md-6 mb-0'),
                Column('card_number', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('card_expiry', css_class='form-group col-md-6 mb-0'),
                Column('cvv', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Field('submit', type='submit', value='Submit', css_class='btn btn-primary')
        )

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        # Add additional validation logic for card number if needed
        return card_number

    def clean_card_expiry(self):
        card_expiry = self.cleaned_data.get('card_expiry')
        # Add validation for expiry date format
        return card_expiry

    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')
        # Add validation for CVV format if necessary
        return cvv


# Vehicle Form
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'  # Adjust this to specify fields if needed


# Booking Form
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'car_registration_number',
            'vehicle_type',
            'time_in',
            'expected_time_out',
            'phone_number',
            'color',
            'parking_lot'
        ]
        widgets = {
            'vehicle_type': forms.Select(choices=[('lorry', 'Lorry'), ('van', 'Van'), ('matatu', 'Matatu'), ('personal', 'Personal')]),
            'parking_lot': forms.Select(),
        }


# Parking Space Form
class ParkingSpaceForm(forms.ModelForm):
    class Meta:
        model = ParkingSpace
        fields = [
            'name',
            'location',
            'pin',
            'phone_number',
            'opening_time',
            'closing_time',
            'facility_type',
            'photo'
        ]



# In forms.py
from django import forms

# Assuming BaseForm is a custom base class for forms
class MyForm(forms.Form):  # Or forms.ModelForm if you're using a model form
    # Add your form fields
    name = forms.CharField(max_length=100)
    email = forms.EmailField()

    def __init__(self, *args, user=None, **kwargs):
        # Call the parent's __init__ method
        super().__init__(*args, **kwargs)

        # Store the user if needed
        self.user = user

        # Optionally, you can filter the form fields based on the user
        if user:
            # Example: filter fields or add conditional logic based on user
            pass

# In forms.py
class BaseForm(forms.Form):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user


from django import forms
from .models import ParkingLoader

class ParkingLoaderForm(forms.ModelForm):
    class Meta:
        model = ParkingLoader
        fields = ['vehicle_type', 'car_registration_number', 'other_field_1', 'other_field_2']
"""