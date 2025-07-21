from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import CustomLoginForm
from .forms import RegisterForm
from .models import Profile

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
                return redirect('main_menu')
            else:
                error = 'Invalid username or password'

    return render(request, 'accounts/login.html', {'form': form, 'error': error})

# Register view (δημιουργεί νέο χρήστη)
def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)

        # Ορισμός password με ασφάλεια
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        phone = form.cleaned_data['phone']
        Profile.objects.create(user=user, phone=phone)
        return redirect('login')  # ή main_menu

    return render(request, 'accounts/register.html', {'form': form})

