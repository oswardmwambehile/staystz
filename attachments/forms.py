from django import forms
from .models import Attachment


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = [
            'attachment_type',
            'nida_number',
            'passport_number',
            'voter_id_number',
            'driving_license_number',
            'document'
        ]

        widgets = {
            'attachment_type': forms.Select(attrs={
                'class': 'form-control'
            }),

            'nida_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter NIDA number'
            }),

            'passport_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Passport number'
            }),

            'voter_id_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Voter ID number'
            }),

            'driving_license_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Driving License number'
            }),

            'document': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.jpg,.jpeg,.png,.pdf'
            }),
        }

    # 🔥 FULL VALIDATION
    def clean(self):
        cleaned_data = super().clean()

        attachment_type = cleaned_data.get('attachment_type')

        nida_number = cleaned_data.get('nida_number')
        passport_number = cleaned_data.get('passport_number')
        voter_id_number = cleaned_data.get('voter_id_number')
        driving_license_number = cleaned_data.get('driving_license_number')

        errors = {}

        if attachment_type == 'nida' and not nida_number:
            errors['nida_number'] = "NIDA number is required."

        elif attachment_type == 'passport' and not passport_number:
            errors['passport_number'] = "Passport number is required."

        elif attachment_type == 'voter_id' and not voter_id_number:
            errors['voter_id_number'] = "Voter ID number is required."

        elif attachment_type == 'driving_license' and not driving_license_number:
            errors['driving_license_number'] = "Driving License number is required."

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data