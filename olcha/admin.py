from django.contrib import admin

from olcha.models import Category, Group, Product

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

