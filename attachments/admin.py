from django.contrib import admin
from django.utils.html import format_html
from .models import Attachment


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):

    # 🔥 ALWAYS show latest first
    ordering = ('-created_at', '-id')

    # 🔹 Columns
    list_display = (
        'user',
        'attachment_type',
        'display_id_number',
        'is_verified',
        'preview',
        'created_at',
    )

    # 🔹 Filters
    list_filter = (
        'attachment_type',
        'is_verified',
        'created_at',
    )

    # 🔹 Search
    search_fields = (
        'user__username',
        'user__email',
        'nida_number',
        'passport_number',
        'voter_id_number',
        'driving_license_number',
    )

    # 🔹 Read-only
    readonly_fields = (
        'created_at',
        'preview',
    )

    # 🔹 Layout
    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),

        ('Attachment Details', {
            'fields': (
                'attachment_type',
                'nida_number',
                'passport_number',
                'voter_id_number',
                'driving_license_number',
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

    # 🔹 Actions
    actions = ['mark_verified', 'mark_unverified']

    # =====================================
    # ✅ FORCE ORDERING (100% GUARANTEED)
    # =====================================
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-created_at', '-id')

    # =====================================
    # ✅ DYNAMIC ID DISPLAY
    # =====================================
    def display_id_number(self, obj):
        if obj.attachment_type == 'nida':
            return obj.nida_number
        elif obj.attachment_type == 'passport':
            return obj.passport_number
        elif obj.attachment_type == 'voter_id':
            return obj.voter_id_number
        elif obj.attachment_type == 'driving_license':
            return obj.driving_license_number
        return "-"

    display_id_number.short_description = "ID Number"

    # =====================================
    # ✅ FILE PREVIEW (IMAGE + PDF)
    # =====================================
    def preview(self, obj):
        if obj.document:
            file_url = obj.document.url.lower()

            if file_url.endswith(('.jpg', '.jpeg', '.png')):
                return format_html(
                    '<img src="{}" style="max-height:120px; border-radius:6px;" />',
                    obj.document.url
                )
            else:
                return format_html(
                    '<a href="{}" target="_blank" style="color:#0ea5e9; font-weight:500;">View File</a>',
                    obj.document.url
                )

        return "No File"

    preview.short_description = "Preview"

    # =====================================
    # ✅ SHOW ONLY RELEVANT FIELD
    # =====================================
    def get_fields(self, request, obj=None):
        fields = ['user', 'attachment_type']

        if obj:
            if obj.attachment_type == 'nida':
                fields.append('nida_number')
            elif obj.attachment_type == 'passport':
                fields.append('passport_number')
            elif obj.attachment_type == 'voter_id':
                fields.append('voter_id_number')
            elif obj.attachment_type == 'driving_license':
                fields.append('driving_license_number')

        fields += ['document', 'preview', 'is_verified', 'created_at']
        return fields

    # =====================================
    # ✅ ACTIONS
    # =====================================
    def mark_verified(self, request, queryset):
        queryset.update(is_verified=True)

    mark_verified.short_description = "✅ Mark selected as VERIFIED"

    def mark_unverified(self, request, queryset):
        queryset.update(is_verified=False)

    mark_unverified.short_description = "❌ Mark selected as UNVERIFIED"