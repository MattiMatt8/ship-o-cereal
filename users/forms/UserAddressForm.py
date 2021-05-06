from django.forms import widgets, ModelForm
from users.models import Country, Address


class UserAddressForm(ModelForm):
    class Meta:
        FIELD_STYLE = "border border-customGray rounded px-4 shadow-inner w-full h-8 placeholder-gray-300 focus:outline-none"

        model = Address
        fields = ("street_name", "country", "additional_comments", "zip", "city")
        widgets = {
            "street_name": widgets.TextInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "123 Main Street, Unit 21"
                }
            ),
            "country": widgets.Select(
                attrs={
                    "class": FIELD_STYLE
                },
                choices=[(None,"Select country")] + [(i.country,i.country) for i in Country.objects.all()]
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

