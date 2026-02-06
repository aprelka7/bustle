from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('phone', 'first_name', 'last_name', 'country')
    list_filter = ('country',)
    search_fields = ('phone', 'first_name', 'last_name',
                     'city', 'country')
    ordering = ('phone',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'address1',
                       'address2', 'city', 'country', 'postal_code',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'first_name', 'last_name', 'password1',
                       'password2', 'is_staff', 'is_active'),
        }),
    )


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'username' in form.base_fields:
            form.base_fields['username'].disabled = True

        return form
    

admin.site.register(CustomUser, CustomUserAdmin)