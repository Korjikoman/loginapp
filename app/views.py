from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.models import User

def main(request):
    
    return render(request, 'app/main_page.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username,
                            password=password)
        if user is not None:
            messages.success(request, ("Succesfully logged in!"))
            login(request, user)
            return redirect('main_page') # Redirect to a success page.
        else:
            messages.success(request, ("We don't know such user, try again!!!!!!!"))
            return redirect('login_page')
    else:
        return render(request, 'app/login_page.html', {})

def logout_user(request):
    logout(request)
    return render(request, 'app/login_page.html', {})

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
    

        