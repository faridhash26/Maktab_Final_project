from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.contrib.auth import get_user_model
# Register your models here.

CustomUser =get_user_model()

class CustomUserAdmin(BaseUserAdmin):

    model = CustomUser
    
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email','username' ,'password','user_type','phone','address','city','zip','image' ,'is_register')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2', 'is_staff', 'is_active','user_type','phone','address','city','zip','image' ,'is_register')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    def image_tag(self, obj):
        if (obj.image):
            return format_html('<img src="{}" idth=50 height=50/>',obj.image.url)
        return '-'


    list_display = ('username','email','user_type', 'is_staff', 'is_active','image_tag' ,'is_register' , 'phone')



admin.site.register(CustomUser, CustomUserAdmin)

