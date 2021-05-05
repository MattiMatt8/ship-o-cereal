from django.forms import widgets, ModelForm
from users.models import Card


class UserCardForm(ModelForm):
    class Meta:
        FIELD_STYLE = "border border-customGray rounded py-3 px-4 shadow-inner w-full h-8 placeholder-gray-300 focus:outline-none"

        model = Card
        fields = ("name", "number", "expiration_date")
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
