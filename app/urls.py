from django.urls import path
from . import views


urlpatterns = [
    path('', views.welcome_page, name='welcome_page'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('main_page/', views.main, name='main_page'),
    path('register/', views.register, name='register'),
    
]