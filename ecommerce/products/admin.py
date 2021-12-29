from django.contrib import admin
from .models import  Category,Tag,Product,Comment
from django.utils.html import format_html

# Register your models here.
@admin.action(description='Mark selected is_published to active ')
def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)

@admin.action(description='Mark selected is_published to deactive ')
def make_published_False(modeladmin, request, queryset):
    queryset.update(is_published=False)

@admin.register(Product)
class ShopAdmin(admin.ModelAdmin):



    def image_tag(self, obj):
        if (obj.image):
            return format_html('<img src="{}" idth=50 height=50/>',obj.image.url)
        return '-'
    list_display = ('name','price','weight', 'stock', 'shop','is_published','image_tag',)
    actions = [make_published ,make_published_False]





admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)