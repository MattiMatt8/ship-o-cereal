from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import widgets
from django.contrib.auth import password_validation
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    FIELD_STYLE = "border border-customGray rounded-full px-6 shadow-inner w-full h-8 placeholder-gray-300 focus:outline-none"

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": FIELD_STYLE,
                "placeholder": "5812345"
            }
        ),
        max_length=255
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": FIELD_STYLE,
                "placeholder": "***********",
                "autocomplete": "new-password",
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={
                "class": FIELD_STYLE,
                "placeholder": "***********",
                "autocomplete": "new-password"
            }
        ),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )


    def clean_first_name(self):
        if self.cleaned_data["first_name"] == "":
            raise ValidationError("This field is required.")
        return self.cleaned_data["first_name"]


    def clean_last_name(self):
        if self.cleaned_data["last_name"] == "":
            raise ValidationError("This field is required.")
        return self.cleaned_data["last_name"]


    def clean_email(self):
        if self.cleaned_data["email"] == "":
            raise ValidationError("This field is required.")
        return self.cleaned_data["email"]


    class Meta:
        FIELD_STYLE = "border border-customGray rounded-full px-6 shadow-inner w-full h-8 placeholder-gray-300 focus:outline-none"

        model = User
        fields = ("username", "first_name", "last_name", "email")
        field_classes = {"username": UsernameField}
        widgets = {
            "username": widgets.TextInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "bobross"
                }
            ),
            "first_name": widgets.TextInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "Bob",
                    "required": ""
                }
            ),
            "last_name": widgets.TextInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "Ross",
                    "required": ""
                }
            ),
            "email": widgets.EmailInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "bob.ross@shipocereal.com",
                    "required": ""
                }
            )
        }
