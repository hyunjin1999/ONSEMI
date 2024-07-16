from django.contrib import admin
from .models import Category, Product
from .forms import CategoryForm 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm 
    list_display = ['name', 'slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']