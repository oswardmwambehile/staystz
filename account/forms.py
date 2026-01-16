from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import User
import re


class RegistrationForm(forms.ModelForm):
    # Password fields with required=True
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter strong password"
        }),
        label="Password",
        required=True
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm password"
        }),
        label="Confirm Password",
        required=True
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "location",
            "user_type",
            "nida_number",
            "nida_card",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
            "location": forms.Select(attrs={"class": "form-select"}),
            "user_type": forms.Select(attrs={"class": "form-select"}),
            "nida_number": forms.TextInput(attrs={"class": "form-control"}),
            "nida_card": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields required at form level (server-side validation)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True
        self.fields["phone_number"].required = True
        self.fields["location"].required = True
        self.fields["user_type"].required = True

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get("user_type")
        nida_number = cleaned_data.get("nida_number")
        nida_card = cleaned_data.get("nida_card")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Require NIDA fields for property owners
        if user_type == "property_owner":
            if not nida_number:
                self.add_error("nida_number", "NIDA Number is required for property owners.")

            if nida_number and not re.fullmatch(r"^[0-9]{20}$", nida_number):
                self.add_error("nida_number", "NIDA number must be exactly 20 digits.")

            if not nida_card:
                self.add_error("nida_card", "Upload your NIDA card image.")

        # Password validation
        if password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        if password:
            if len(password) < 8:
                self.add_error("password", "Password must be at least 8 characters long.")
            if not re.search(r"[A-Z]", password):
                self.add_error("password", "Password must contain at least one uppercase letter.")
            if not re.search(r"[a-z]", password):
                self.add_error("password", "Password must contain at least one lowercase letter.")
            if not re.search(r"[0-9]", password):
                self.add_error("password", "Password must contain at least one digit.")
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                self.add_error("password", "Password must contain at least one special character.")

            validate_password(password)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        user.set_password(password)
        user.user_verified = False
        if commit:
            user.save()
        return user



from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email",
            "required": True
        }),
        label="Email"
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password",
            "required": True
        }),
        label="Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            # Authenticate using email and password
            user = authenticate(username=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid email or password.")
            elif not user.is_active:
                raise forms.ValidationError("This account is inactive.")
            
            # Store the user object for use in the view
            self.user = user

        return cleaned_data





from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class SecurePasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter current password"}),
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter new password"}),
        help_text="Your password must be strong: minimum 8 characters, mix of letters, numbers, and symbols.",
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm new password"}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password):
            raise ValidationError("Your current password was entered incorrectly.")
        return old_password

    def clean_new_password1(self):
        password = self.cleaned_data.get("new_password1")
        validate_password(password, self.user)  # Django's built-in validators
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("The two new password fields didn’t match.")
        return cleaned_data

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user



