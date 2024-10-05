from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm


def main(request):
    return render(request, 'app/main_page.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username,
                            password=password)
        if user is not None:
            login(request, user)
            return redirect('main_page') # Redirect to a success page.
        else:
            messages.success(request, ("We don't know such user, try again!!!!!!!"))
            return redirect('login_user')
    else:
        return render(request, 'app/login_page.html', {})

def logout_user(request):
    logout(request)
    return render(request, 'app/login_page.html', {})

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect('login_user')
    else: 
        form = RegisterForm()
        return render(response, "app/register.html", {'form' : form })
    

        