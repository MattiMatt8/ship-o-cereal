from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
from django import forms
from django.forms import widgets
from django.contrib.auth import password_validation
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    FIELD_STYLE = "border border-customGray rounded-full py-3 px-6 shadow-inner w-full h-8 focus:outline-none"

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": FIELD_STYLE,
                "placeholder": "Bob"
            }
        ),
        max_length=255
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": FIELD_STYLE,
                "placeholder": "Ross"
            }
        ),
        max_length=255
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": FIELD_STYLE,
                "placeholder": "5812345"
            }
        ),
        max_length=255
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": FIELD_STYLE,
                "placeholder": "bob.ross@shipocereal.com"
            }
        ),
        max_length=255
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        FIELD_STYLE = "border border-customGray rounded-full py-3 px-6 shadow-inner w-full h-8 focus:outline-none"

        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}
        widgets = {
            "username": widgets.TextInput(
                attrs={
                    "class": FIELD_STYLE
                }
            )
        }

    #
    #
    #
    #
    # username = UsernameField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": FIELD_STYLE,
    #             'autofocus': True
    #         }
    #     )
    # )
    # password = forms.CharField(
    #     label=_("Password"),
    #     strip=False,
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "class": FIELD_STYLE,
    #             'autocomplete': 'current-password'
    #         }
    #     ),
    # )
