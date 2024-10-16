from django.urls import path
from . import views
from .views import ResetPasswordView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.welcome_page, name='welcome_page'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('main_page/', views.main, name='main_page'),
    path('register/', views.register, name='register'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uid64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="registr/password_reset_confirm.html"), name='password_reset_confirm' ),
    path('password-reset-comlete/', auth_views.PasswordResetCompleteView.as_view(template_name="registr/password_reset_complete.html"))
]