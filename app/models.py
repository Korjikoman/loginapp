from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.contrib.auth.models import PermissionsMixin

class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=100)
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    registered_date = models.DateTimeField(default=timezone.now)
    

    subscripted = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def subscribe(self):
        self.subscripted = True
        self.save()
    
    def __str__(self):
        return self.email

class Notification(models.Model):
    message = models.CharField(max_length = 100);
    
    def __str__(self):
        return self.message