from django.contrib import admin
from .models import Dish, Category, DishImage, Allergen


class DishImageInLine(admin.TabularInline):
    model = DishImage
    extra = 1

class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'category', 'price']
    list_filter = ['category', 'allergens']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['allergens']
    inlines = [DishImageInLine]

class Category_Admin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class AllergenAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Allergen, AllergenAdmin)
admin.site.register(Category, Category_Admin)
admin.site.register(Dish, DishAdmin)