from django.contrib import admin
from .models import Order,OrderItem
# Register your models here.

@admin.register(Order)
class CusomtOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'customer','createdAt', 'totalPrice',)
    fieldsets = (
        (None, {'fields': ('status','customer' ,'createdAt','updated_at','taxPrice','totalPrice')}),
        # ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    readonly_fields = ['createdAt','updated_at']

@admin.register(OrderItem)
class CusomtOrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'order','qty', 'price',)