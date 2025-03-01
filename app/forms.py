from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from .models import Users
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterForm(UserCreationForm):

    username = forms.CharField(min_length=5, max_length=15)
    email = forms.EmailField(widget=forms.EmailInput)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
        
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].label= ''
        
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email = email)
        if new.count():
            raise ValidationError("Email already exists!!!")
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        print(password1, password2)
        if password1 and password2 and password2 != password1:
            raise ValidationError("Password don't match!!!")
            
        return password2
    
    def save(self, commit=True):
        user =User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password2']
            
        )
        return user

class Login_user(AuthenticationForm):
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(Login_user, self).__init__( *args, **kwargs)
        
    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control',
            'placeholder': 'your username',
            'id': 'hello',
        }
    ))
        
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder':'your password',
            'id':'hi'
        }
    ))
    
        
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError('This account is inactive',
                                code="inactive")
    