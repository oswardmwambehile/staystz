from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


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

    # ID Numbers (only one required depending on type)
    nida_number = models.CharField(max_length=30, blank=True, null=True)
    passport_number = models.CharField(max_length=30, blank=True, null=True)
    voter_id_number = models.CharField(max_length=30, blank=True, null=True)
    driving_license_number = models.CharField(max_length=30, blank=True, null=True)

    # File (PDF + Images)
    document = models.FileField(
        upload_to='attachments/documents/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'pdf']
            )
        ]
    )

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    # 🔥 VALIDATION
    def clean(self):
        errors = {}

        if self.attachment_type == 'nida':
            if not self.nida_number:
                errors['nida_number'] = "NIDA number is required."

        elif self.attachment_type == 'passport':
            if not self.passport_number:
                errors['passport_number'] = "Passport number is required."

        elif self.attachment_type == 'voter_id':
            if not self.voter_id_number:
                errors['voter_id_number'] = "Voter ID number is required."

        elif self.attachment_type == 'driving_license':
            if not self.driving_license_number:
                errors['driving_license_number'] = "Driving License number is required."

        if errors:
            raise ValidationError(errors)

    # 🔥 CLEAN UNUSED FIELDS (IMPORTANT)
    def save(self, *args, **kwargs):
        if self.attachment_type != 'nida':
            self.nida_number = None

        if self.attachment_type != 'passport':
            self.passport_number = None

        if self.attachment_type != 'voter_id':
            self.voter_id_number = None

        if self.attachment_type != 'driving_license':
            self.driving_license_number = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.get_attachment_type_display()}"