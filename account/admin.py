from django.contrib import admin
from .models import User, OtpToken
from django.contrib.auth.admin import UserAdmin

# ✅ THIS IS THE CORRECT PLACE
admin.site.site_header = "StayTanzania Administration"
admin.site.site_title = "StayTanzania Admin Portal"
admin.site.index_title = "Welcome to StayTanzania Administration"


class CustomUserAdmin(UserAdmin):
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