from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import RegisterForm
from .models import Users, Notification

class CustomUserAdmin(UserAdmin):
    add_form = RegisterForm
    list_display = ('email', 'is_admin', 'subscripted')
    list_filter = ('is_admin')
    fieldsets = (
        (None, {'fields': ('email, password', 'subscripted')}),
        ('Permissions', {'fields': ('is_admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'subscripted'),
        }),
    )
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Users)
admin.site.register(Notification)