from django.urls import path
from . import views


urlpatterns = [
    path('login_user/', views.login_user, name='login_user'),
    path('main_page/', views.main, name='main_page'),
    path('register/', views.register, name='register'),
]