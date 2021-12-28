from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
# Register your models here.
# from .models import CustomUser
CustomUser =get_user_model()

class CustomUserAdmin(BaseUserAdmin):

    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username','email','user_type', 'is_staff', 'is_active','image')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email','username' ,'password','user_type','phone','address','city','zip')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2', 'is_staff', 'is_active','user_type','phone','address','city','zip','image')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)





# from django.contrib import admin
# from django.contrib.auth.forms import AdminPasswordChangeForm
# from .models import User
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.utils.translation import ugettext_lazy as _
# class UserAdmin(BaseUserAdmin):
# list_display = ['email', 'is_staff']
# change_password_form = AdminPasswordChangeForm
# ordering = ('email',)
# add_fieldsets = (
# (None, {
# 'classes': ('wide',),
# 'fields': ('email', 'full_name', 'password1', 'password2')
# }),
# )
# fieldsets = (
# ,mport UserAdmin as BaseUserAdmin
# from django.utils.translation import ugettext_lazy as _
# class UserAdmin(BaseUserAdmin):
# list_display = ['email', 'is_staff']
# change_password_form = AdminPasswordChangeForm
# ordering = ('email',)
# add_fieldsets = (
# (None, {
# 'classes': ('wide',),
# 'fields': ('email', 'full_name', 'password1', 'password2')
# }),
# )
# fieldsets = (
# (_('authentication data'), {
# "fields": (
# 'email',
# 'password',
# ),
# }),
# (_('Personal info'), {
# "fields": ('full_name', 'avatar')
# }),
# (_('Permissions'), {
# "fields": ('is_author','is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')
# }),
# (_('Important dates'), {
# "fields": ('last_login',)
# }),
# )
# # Register your models here.
# admin.site.register(User, UserAdmin