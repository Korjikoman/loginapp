from django.db import models
from django.conf import settings
from django.utils import timezone


class Login(models.Model):
    email = models.CharField(max_length=100)
    username = models.CharField(max_length=200)
    password = models.TextField(max_length=200)
    registered_date = models.DateTimeField(default=timezone.now)
    is_registered = models.BooleanField()
    
    def register(self):
        self.is_registered = True
        self.save()
    
    def __str__(self):
        return self.username
    
    