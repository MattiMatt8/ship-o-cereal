from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
from django import forms


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'flex'}),
    )
