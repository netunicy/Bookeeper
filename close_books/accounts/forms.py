import re
from django import forms
from django.contrib.auth.models import User

class CustomLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=200)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    phone = forms.CharField(max_length=25, label="Phone Number")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']  # username υποχρεωτικό

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        username = cleaned_data.get("username")

        if password and password2:
            if password != password2:
                raise forms.ValidationError("Passwords do not match.")

            if username and User.objects.filter(username=username).exists():
                raise forms.ValidationError("This username is already taken. Please choose another one.")

            if len(password) < 9:
                raise forms.ValidationError("Password must be at least 9 characters long.")

            if not re.search(r'[A-Z]', password):
                raise forms.ValidationError("Password must contain at least one uppercase letter.")

            if not re.search(r'[a-z]', password):
                raise forms.ValidationError("Password must contain at least one lowercase letter.")

            if not re.search(r'[0-9]', password):
                raise forms.ValidationError("Password must contain at least one number.")

            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                raise forms.ValidationError("Password must contain at least one special character.")

            if not all(ord(c) < 128 for c in password):
                raise forms.ValidationError("Password must contain only Latin characters and common ASCII symbols.")

        return cleaned_data

class SendUsernameForm(forms.Form):
    email = forms.EmailField(label="Email address", max_length=254, widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email',
    }))

    
class CustomOtpForm(forms.Form):
    otp = forms.CharField(label='OTP - One Time Password', max_length=200)