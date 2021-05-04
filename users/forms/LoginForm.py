from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
from django import forms


class LoginForm(AuthenticationForm):
    FIELD_STYLE = "border border-customGray rounded-full py-3 px-6 shadow-inner w-full h-8 focus:outline-none"

    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "placeholder": "Bob",
                "class": FIELD_STYLE
            }
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "***********",
                "class": FIELD_STYLE
            }
        ),
    )
