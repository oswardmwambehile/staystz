from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


class Attachment(models.Model):

    ATTACHMENT_TYPE_CHOICES = [
        ('nida', 'NIDA'),
        ('passport', 'Passport'),
        ('driving_license', 'Driving License'),
        ('voter_id', 'Voter ID'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attachments'
    )

    attachment_type = models.CharField(
        max_length=20,
        choices=ATTACHMENT_TYPE_CHOICES
    )

    # Required only when attachment_type = NIDA
    nida_number = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    # Image only (NOT file)
    document = models.ImageField(
        upload_to='attachments/images/'
    )

    is_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.attachment_type == 'nida' and not self.nida_number:
            raise ValidationError("NIDA number is required for NIDA attachment.")

    def __str__(self):
        return f"{self.user} - {self.get_attachment_type_display()}"
