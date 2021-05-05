from django import forms
from django.forms import widgets, ModelForm
from django.contrib.auth.models import User


class UpdateUserForm(ModelForm):
    FIELD_STYLE = "border border-customGray rounded py-3 px-4 shadow-inner w-full h-8 placeholder-gray-300 focus:outline-none"

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": FIELD_STYLE,
                "placeholder": "5812345"
            }
        ),
        max_length=255
    )
    picture = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": FIELD_STYLE,
                "placeholder": "https://imgur.com/my_image.png"
            }
        ),
        max_length=255,
        required=False
    )
    class Meta:
        FIELD_STYLE = "border border-customGray rounded py-3 px-4 shadow-inner w-full h-8 placeholder-gray-300 focus:outline-none"

        model = User
        fields = ("first_name", "last_name", "email")
        widgets = {
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
