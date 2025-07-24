from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CustomLoginForm,SendUsernameForm
from .forms import RegisterForm, CustomOtpForm
from .models import Profile,Otp
from django.views.decorators.csrf import csrf_exempt, csrf_protect,requires_csrf_token
from django.core.mail import send_mail
import random
from django.contrib.auth import get_user_model
from django.contrib import messages
import mailtrap as mt

@requires_csrf_token
@csrf_protect
def custom_login_view(request):
    form = CustomLoginForm(request.POST or None)
    error = None

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            user_id = user.id
            request.session['user_id'] = user.id


            if user is not None:
                otp = random.randint(100000, 999999)

                # Απόκτηση του email του χρήστη με ασφάλεια
                email = user.email
                request.session['user_email'] = email
                
                mail = mt.Mail(
                        sender=mt.Address(email="hello@cp-accounting.com", name="OTP for Login"),
                        to=[mt.Address(email=email)],
                        subject="Your OTP Code for Account Login",
                        text="OTP Password is " + str(otp),
                        category="OTP for Login",
                    )

                client = mt.MailtrapClient(token="d496560ab3270434f34280336868cc7d")
                client.send(mail)

                Otp.objects.update(otp=otp)
                return redirect('accounts:check_otp')
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
        
        mail = mt.Mail(
            sender=mt.Address(email="hello@cp-accounting.com", name="OTP for Register"),
            to=[mt.Address(email=email)],
            subject="Your OTP Code for Account Register",
            text="OTP Password is " + str(otp),
            category="OTP for Register",
            )

        client = mt.MailtrapClient(token="d496560ab3270434f34280336868cc7d")
        client.send(mail)

        return redirect('accounts:check_otp')

    return render(request, 'accounts/register.html', {'form': form})

@requires_csrf_token
@csrf_protect
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
            login(request, user)
            return redirect('main_menu:main_menu')
        else:
            messages.add_message(request, messages.INFO, "Invalid OTP code.")
            return redirect('accounts:check_otp')
            

    return render(request, 'accounts/otp.html', {'form': form})

@requires_csrf_token
@csrf_protect
def resend_otp(request):

    user_email = request.session.get('user_email')
    user_id = request.session.get('user_id')
    otp = random.randint(100000, 999999)
    Otp.objects.update(otp=otp)
    mail = mt.Mail(
        sender=mt.Address(email="hello@cp-accounting.com", name="OTP for Login"),
        to=[mt.Address(email=user_email)],
        subject="Your OTP Code for Account Login",
        text="OTP Password is " + str(otp),
        category="OTP for Login",
        )

    client = mt.MailtrapClient(token="d496560ab3270434f34280336868cc7d")
    client.send(mail)
    
    messages.add_message(request, messages.INFO, "A new OTP has been sent to your email.")
    return redirect('accounts:check_otp')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@requires_csrf_token
@csrf_protect
def forgot_username(request):
    if request.method == "POST":
        form = SendUsernameForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = User.objects.filter(email=email)
            if users.exists():
                for user in users:
                    username = user.username
                    text = f'For your account the username is: {username}'
                    send_mail(
                        subject="Your Username",
                        message=text,
                        from_email="noreply@example.com",
                        recipient_list=[email],
                    )
                return render(request, 'send_username_done.html')
            else:
                messages.error(request, 'The email you entered is not associated with any account. Please check the email and try again!')
        # Εμφανίζεται και το form με λάθη αν έχει
        return render(request, 'send_username.html', {'form': form})
    else:
        form = SendUsernameForm()
        return render(request, 'send_username.html', {'form': form})