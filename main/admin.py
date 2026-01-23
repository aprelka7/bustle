from django.contrib import admin
from .models import Dish, Category, DishImage



class DishImageInLine(admin.TabularInline):
    model = DishImage
    extra = 1

class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']
    list_filter = ['category']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [DishImageInLine]

class Category_Admin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, Category_Admin)
admin.site.register(Dish, DishAdmin)