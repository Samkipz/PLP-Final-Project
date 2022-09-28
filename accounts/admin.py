from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, LandlordProfile, TenantProfile
from .form import MyUserCreationForm, MyUserChangeForm

class UserAdmin(UserAdmin):
    add_user_form = MyUserCreationForm
    change_user_form = MyUserChangeForm
    model = User

    list_display = ('email', 'first_name', 'last_name', 'gender', 'is_landlord', 'is_tenant', 'is_active', 'phone_no','avatar')
    list_filter = ('gender', 'is_landlord', 'is_tenant', 'is_active',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'gender', 'phone_no','avatar')}),
        ('Permissions', {'fields': ('is_landlord', 'is_tenant', 'is_active')}),
        ('Important dates', {'fields': ('last_login','date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_landlord', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
admin.site.register(User, UserAdmin)

