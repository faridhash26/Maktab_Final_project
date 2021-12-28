from django.contrib import admin
from .models import Post, Category, Comment, PostTag

# Register your models here.

# admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(PostTag)
class TagAdmin(admin.ModelAdmin):
    pass
