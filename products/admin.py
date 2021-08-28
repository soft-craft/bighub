from django.contrib import admin
from .models import Category,Products

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    #list_display = ['product_name', 'slug', 'description', 'available', 'created', 'updated']
    prepopulated_fields = {'slug': ('product_name',)}


