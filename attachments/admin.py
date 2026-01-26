from django.contrib import admin
from django.utils.html import format_html
from .models import Attachment


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):

    # 🔹 Columns shown in admin list
    list_display = (
        'user',
        'attachment_type',
        'nida_number',
        'is_verified',
        'preview',
        'created_at',
    )

    # 🔹 Filters on right sidebar
    list_filter = (
        'attachment_type',
        'is_verified',
        'created_at',
    )

    # 🔹 Search bar
    search_fields = (
        'user__username',
        'user__email',
        'nida_number',
    )

    # 🔹 Ordering
    ordering = ('-created_at',)

    # 🔹 Read-only fields
    readonly_fields = (
        'created_at',
        'preview',
    )

    # 🔹 Field layout
    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('Attachment Details', {
            'fields': (
                'attachment_type',
                'nida_number',
                'document',
                'preview',
            )
        }),
        ('Verification', {
            'fields': ('is_verified',)
        }),
        ('System Info', {
            'fields': ('created_at',)
        }),
    )

    # 🔹 Admin actions
    actions = ['mark_verified', 'mark_unverified']

    # ✅ Image preview in admin
    def preview(self, obj):
        if obj.document:
            return format_html(
                '<img src="{}" style="max-height:120px; border-radius:6px;" />',
                obj.document.url
            )
        return "No Image"

    preview.short_description = "Document Preview"

    # ✅ Actions
    def mark_verified(self, request, queryset):
        queryset.update(is_verified=True)

    mark_verified.short_description = "Mark selected attachments as VERIFIED"

    def mark_unverified(self, request, queryset):
        queryset.update(is_verified=False)

    mark_unverified.short_description = "Mark selected attachments as UNVERIFIED"
