from django.contrib import admin
from .models import  Category,Tag,Product,Comment
from django.utils.html import format_html

# Register your models here.
@admin.register(Product)
class ShopAdmin(admin.ModelAdmin):



    def image_tag(self, obj):
        if (obj.image):
            return format_html('<img src="{}" idth=50 height=50/>',obj.image.url)
        return '-'
    list_display = ('name','price','weight', 'stock', 'shop','image_tag')





admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)