from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import widgets
from django.contrib.auth import password_validation
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    FIELD_STYLE = "border border-customGray rounded-full py-3 px-6 shadow-inner w-full h-8 focus:outline-none"

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

    class Meta:
        FIELD_STYLE = "border border-customGray rounded-full py-3 px-6 shadow-inner w-full h-8 focus:outline-none"

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
                    "placeholder": "Bob"
                }
            ),
            "last_name": widgets.TextInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "Ross"
                }
            ),
            "email": widgets.EmailInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "bob.ross@shipocereal.com"
                }
            )
        }
