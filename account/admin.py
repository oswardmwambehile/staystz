from django.contrib import admin
from .models import User, OtpToken
from django.contrib.auth.admin import UserAdmin

# ✅ THIS IS THE CORRECT PLACE
admin.site.site_header = "StayTanzania Administration"
admin.site.site_title = "StayTanzania Admin Portal"
admin.site.index_title = "Welcome to StayTanzania Administration"


class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "date_joined", "is_staff")
    ordering = ("-date_joined",)  # 👈 newest users first

    search_fields = ("email", "username")
    list_filter = ("is_staff", "is_superuser", "is_active", "date_joined")

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
         ),
    )


class OtpTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "otp_code")


admin.site.register(OtpToken, OtpTokenAdmin)
admin.site.register(User, CustomUserAdmin)