from django.contrib import admin
from .models import NewsEvent

@admin.register(NewsEvent)
class NewsEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_event', 'author', 'publish_date', 'event_date', 'is_active')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_event', 'is_active')
    ordering = ('-publish_date',)

    def save_model(self, request, obj, form, change):
        # If the object is being created (not updated), set the author to the logged-in user
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)