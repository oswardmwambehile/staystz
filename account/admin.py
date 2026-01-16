# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

admin.site.site_header = "StayStz Admin"
admin.site.site_title = "StayStz Admin Portal"
admin.site.index_title = "Welcome to StayStz Dashboard"

class UserAdmin(BaseUserAdmin):
    model = User

    # Fields to display in list view
    list_display = (
        'email', 
        'first_name', 
        'last_name', 
        'user_type', 
        'location', 
        'user_verified', 
        'phone_number', 
        'nida_number', 
        'is_staff', 
        'is_active',
        'date_joined'
    )

    # Fields you can filter by
    list_filter = (
        'user_type', 
        'location', 
        'user_verified', 
        'is_staff', 
        'is_active'
    )

    # Fields you can search by
    search_fields = ('email', 'first_name', 'last_name', 'phone_number', 'nida_number')

    # Pagination
    list_per_page = 20

    # Default ordering
    ordering = ('-date_joined',)

    # Fields when editing a user
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'location')}),
        ('Verification', {'fields': ('user_verified', 'nida_number', 'nida_card')}),
        ('Permissions', {'fields': ('user_type', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields when creating a user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'user_type', 'is_staff', 'is_active')}
        ),
    )

    # Use email as username field
    ordering = ('email',)

# Register the custom user admin
admin.site.register(User, UserAdmin)
