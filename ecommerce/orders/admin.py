from django.contrib import admin
from .models import Order,OrderItem
# Register your models here.

@admin.register(Order)
class CusomtOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'customer','createdAt', 'totalPrice',)

@admin.register(OrderItem)
class CusomtOrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'order','qty', 'price',)