from django.contrib.auth.forms import UserCreationForm
from .models import User 
from django import forms
from .models import ShippingAddress


class CustomUserForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username'}))
    email=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your email'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter conform password'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class ShippingAddressForm(forms.ModelForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your 10 digit mobile number'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter address'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter state'}))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ZIP code'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter country'}))

    class Meta:
        model = ShippingAddress
        fields = ['phone_number','full_name', 'address', 'city', 'state', 'zip_code', 'country']