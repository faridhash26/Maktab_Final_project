from django.contrib import admin
from .models import Shop
# Register your models here.



@admin.action(description='Mark selected shops to active ')
def make_published(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_type', 'name', 'address', 'is_active',
                        'is_delete', 'author',)
    list_filter = ("name", 'address', 'is_active', 'is_delete','shop_type')
    search_fields = ('name', 'address',)
    list_editable = ('is_active','is_delete')
    actions = [make_published]




