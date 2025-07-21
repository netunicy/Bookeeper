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

        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
    
class CustomOtpForm(forms.Form):
    otp = forms.CharField(label='OTP - One Time Password', max_length=200)