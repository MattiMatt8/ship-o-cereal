from django.forms import widgets, ModelForm
from users.models import Address


class UserAddressForm(ModelForm):
    class Meta:
        FIELD_STYLE = "border border-customGray rounded py-3 px-4 shadow-inner w-full h-8 placeholder-gray-300 focus:outline-none"

        model = Address
        fields = ("address", "country", "additional_comments", "zip", "city")
        widgets = {
            "address": widgets.TextInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "123 Main Street, Unit 21"
                }
            ),
            "country": widgets.TextInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "United States"
                }
            ),
            "zip": widgets.TextInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "10001"
                }
            ),
            "city": widgets.TextInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "New York"
                }
            ),
            "additional_comments": widgets.TextInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "Right door"
                }
            )
        }
