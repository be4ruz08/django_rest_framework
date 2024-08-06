from django.contrib import admin

from olcha.models import Category

# Register your models here.

# admin.site.register(Category)


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}