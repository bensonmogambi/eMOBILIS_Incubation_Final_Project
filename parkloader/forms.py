from django import forms
from .models import parkingLoader,ParkingLot
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.utils.translation import gettext_lazy as _
from .models import Billing
from django.contrib.auth import authenticate
class MyForm(forms.ModelForm):
  
  def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
  parking_lot = forms.ModelChoiceField(queryset=ParkingLot.objects.all())
  class Meta:
    model = parkingLoader
    fields = [ "car_regestration_number","vehicle_type"]
    labels = {'Car registration number': "car_regestration_number", "Vehicle type": "vehicle_type",}

    # def __init__(self, *args, **kwargs):
    #     super(MyForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Row(
    #             Column('parking_lot', css_class='form-group col-md-2 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Row(
    #             Column('car_reg', css_class='form-group col-md-2 mb-0'),
    #             Column('vehicle_type', css_class='form-group col-md-2 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Submit('submit', 'Submit')
    #     )
    #     self.fields['parking_lot'].widget.attrs.update({'class': 'custom-select custom-select-sm'})

class ParkingLotForm(forms.ModelForm):
    class Meta:
        model = ParkingLot
        fields = ['location']
        labels = {'location':'location',}


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
            else:
                if not user.is_active:
                    raise forms.ValidationError(
                        self.error_messages['inactive'],
                        code='inactive',
                    )
        return self.cleaned_data    


class registerForm(UserCreationForm):
   
   class Meta:
        model= User
        fields = ['username','email','password1','password2'] 

   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_show_errors = True
        self.layout = Layout(
            Field('username', placeholder='Username', autofocus=''),
            Field('email', placeholder='Email'),
            Field('password1', placeholder='Password'),
            Field('password2', placeholder='Password confirmation'),
        )        

   def clean_username(self):
        username = self.cleaned_data.get('username')
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")

        # Check if the username is invalid (e.g. contains special characters)
        if not username.isalnum():
            raise forms.ValidationError("Username should only contain letters and numbers.")

        return username    


class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['plan','card_number', 'card_expiry', 'cvv']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

            self.fields['card_number'].widget.attrs.update({
                'placeholder': _('Card Number')
            })

            self.fields['card_expiry'].widget.attrs.update({
          'placeholder': _('Expiration Year')
          })
            self.fields['cvv'].widget.attrs.update({
          'placeholder': _('cvv')
          }) 

