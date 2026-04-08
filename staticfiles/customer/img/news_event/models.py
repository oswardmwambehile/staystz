from django.db import models
from django.conf import settings
from django.utils import timezone

class NewsEvent(models.Model):
    """
    Combined model for News and Events
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    content = models.TextField()
    image = models.ImageField(upload_to='news_events/', blank=True, null=True)
    is_event = models.BooleanField(default=False)  # True = Event, False = News
    publish_date = models.DateTimeField(default=timezone.now)
    event_date = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-publish_date']
        verbose_name = "News & Event"
        verbose_name_plural = "News & Events"

    def __str__(self):
        return f"{'Event' if self.is_event else 'News'}: {self.title}"

    def get_display_date(self):
        """Returns event_date if it's an event, otherwise publish_date"""
        return self.event_date if self.is_event and self.event_date else self.publish_date