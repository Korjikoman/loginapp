from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
            return redirect('main') # Redirect to a success page.
        else:
            messages.success(request, "We don't know such user, try again")
            pass
    else:
        return render(request, 'app/login_page.html', {})

def logout_user(request):
    logout(request)
    return render(request, 'app/login_page.html', {})