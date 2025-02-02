from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, Login_user
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin


class ResetPassword(SuccessMessageMixin,PasswordResetView):
    template_name = 'registr/password_reset_form.html'
    email_template_name = 'registr/password_reset_email.html'
    
    success_message = ''' Check your email box '''
    
    success_url = reverse_lazy('login_user')



def welcome_page(request):
    return render(request, 'app/welcome_page.html')


def main(request):
    return redirect('transcribe_audio')
    
def login_user(request):
    if request.method == 'POST':
        form = Login_user(data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username= username, password = password)
            print(user)
            if user is not None:
                login(request, user)
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
    messages.success(request, ('You have been logged out'))
    return redirect('login_user')

def register(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
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
    

        