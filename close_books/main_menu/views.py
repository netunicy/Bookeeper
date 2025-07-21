from django.shortcuts import render,redirect

def main_menu(request):
    return render (request,'main_menu.html')