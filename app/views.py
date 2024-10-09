from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, Login_user
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


def welcome_page(request):
    return render(request, 'app/welcome_page.html')

def main(request):
    return render(request, 'app/main_page.html')

def login_user(request):
    if request.method == 'POST':
        form = Login_user(data=request.POST)
        if form.is_valid():
            messages.success(request, ("Successfully logged in!"))
            return redirect('main_page')
        else:
            messages.success(request, ("We don't know such user, try again!!!!!!!"))
            return redirect('login_user')
    else:
        form = Login_user()
        return render(request, 'app/login_page.html', {'form' : form})

def logout_user(request):
    logout(request)
    return redirect('login_user')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Success"))
            return redirect('main_page')
        else:
            
            return render(request, "app/register.html", {'form' : form, 'errors': form.errors})
    else: 
        print("else")
        form = RegisterForm()
        return render(request, "app/register.html", {'form' : form })
    

        