from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='username', min_length=5, max_length=15)
    print(f"username = {username}")
    email = forms.EmailField(label='email')
    password1 = forms.CharField( label='password', widget=forms.PasswordInput)
    password2 = forms.CharField( label='Confirm password', widget=forms.PasswordInput)
    
    def email_check(self):
        email = self.cleaned_data['email'].lower()
        print(email)
        new = User.objects.filter(email = email)
        if new.count():
            raise ValidationError("Email already exists")
        return email
    
    def password_check(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        print(password1, password2)
        if password1 and password2 and password2 != password1:
            raise ValidationError("Password don't match")
        return password2
    
    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password2']
            
        )
        return user