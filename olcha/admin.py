from django.contrib import admin

from olcha.models import Category, Group, Product, Image, Comment

# Register your models here.

# admin.site.register(Category)


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Group)
class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Product)
class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('message', 'rating', 'created_at')
    search_fields = ('message',)
    list_filter = ('rating', 'created_at')


admin.site.register(Image)