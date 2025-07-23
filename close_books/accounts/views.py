from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import CustomLoginForm
from .forms import RegisterForm, CustomOtpForm
from .models import Profile,Otp
from django.views.decorators.csrf import csrf_exempt, csrf_protect,requires_csrf_token
from django.core.mail import send_mail
import random
from django.contrib.auth import get_user_model
from django.contrib import messages

@requires_csrf_token
@csrf_protect
def custom_login_view(request):
    form = CustomLoginForm(request.POST or None)
    error = None

    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('main_menu:main_menu')
            else:
                error = 'Invalid username or password'

    return render(request, 'accounts/login.html', {'form': form, 'error': error})

@requires_csrf_token
@csrf_protect
def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)

        user.is_active = False

        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()

        request.session['user_id'] = user.id

        phone = form.cleaned_data['phone']
        email = form.cleaned_data['email']
        request.session['user_email'] = email
        
        otp = random.randint(100000, 999999)

        Profile.objects.create(user=user, phone=phone)
        Otp.objects.create(user=user,otp=otp)
        
        send_mail(
            subject="OTP Password",
            message="OTP Password is " + str(otp),
            from_email="noreply@example.com",
            recipient_list=[email],
            )

        return redirect('accounts:check_otp')

    return render(request, 'accounts/register.html', {'form': form})

def check_otp(request):

    form = CustomOtpForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user_id = request.session.get('user_id')
        otp = form.cleaned_data['otp']
        otp_valid = Otp.objects.filter(user=user_id, otp=otp).exists()
        if otp_valid:
            User = get_user_model()
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            return redirect('main_menu:main_menu')
        else:
            return render(request, 'accounts/otp.html', {'form': form})
            

    return render(request, 'accounts/otp.html', {'form': form})

def resend_otp(request):
    user_email = request.session.get('user_email')
    user_id = request.session.get('user_id')
    otp = random.randint(100000, 999999)
    Otp.objects.update(otp=otp)
    send_mail(
        subject="OTP Password",
        message="OTP Password is " + str(otp),
        from_email="noreply@example.com",
        recipient_list=[user_email],
        )
    
    messages.add_message(request, messages.INFO, "A new OTP has been sent to your email.")
    return redirect('accounts:check_otp')