from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets, ModelForm
from django.contrib.auth.models import User


class UpdateUserForm(ModelForm):
    FIELD_STYLE = "border border-customGray rounded px-4 shadow-inner w-full h-8 placeholder-gray-300 focus:outline-none"

    phone = forms.CharField(
        widget=forms.TextInput(attrs={"class": FIELD_STYLE, "placeholder": "5812345"}),
        max_length=255,
    )

    picture = forms.ImageField(required=False)

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
        FIELD_STYLE = "border border-customGray rounded px-4 shadow-inner w-full h-8 placeholder-gray-300 focus:outline-none"

        model = User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": widgets.TextInput(
                attrs={"class": FIELD_STYLE, "placeholder": "Bob", "required": ""}
            ),
            "last_name": widgets.TextInput(
                attrs={"class": FIELD_STYLE, "placeholder": "Ross", "required": ""}
            ),
            "email": widgets.EmailInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "bob.ross@shipocereal.com",
                    "required": "",
                }
            ),
        }
