from django.urls import path
from . import views


urlpatterns = [
    path('login_page/', views.login_user, name='login_page'),
    path('main_page/', views.main, name='main_page'),
    
]