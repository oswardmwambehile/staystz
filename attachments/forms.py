from django import forms
from .models import Attachment


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['attachment_type', 'nida_number', 'document']

        widgets = {
            'attachment_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'nida_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter NIDA number'
            }),
            'document': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        attachment_type = cleaned_data.get('attachment_type')
        nida_number = cleaned_data.get('nida_number')

        if attachment_type == 'nida' and not nida_number:
            raise forms.ValidationError("NIDA number is required.")

        return cleaned_data
