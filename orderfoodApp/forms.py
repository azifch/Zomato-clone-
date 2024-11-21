from django.contrib.auth.forms import UserCreationForm
from django import forms  
from django.contrib.auth.models import User
from .models import Booking

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['restaurant', 'user', 'name', 'email', 'phone_no', 'date', 'time', 'people_size']