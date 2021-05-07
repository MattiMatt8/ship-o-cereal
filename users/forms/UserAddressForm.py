from django.forms import widgets, ModelForm
from users.models import Country, Address


class UserAddressForm(ModelForm):
    class Meta:
        FIELD_STYLE = "border border-customGray rounded px-4 shadow-inner w-full h-8 placeholder-gray-300 focus:outline-none"

        model = Address
        fields = ("street_name", "house_number", "country", "additional_comments", "zip", "city")
        widgets = {
            "street_name": widgets.TextInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "Varick Street"
                }
            ),
            "house_number": widgets.NumberInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "121"
                }
            ),
            "country": widgets.Select(
                attrs={
                    "class": FIELD_STYLE
                },
                choices=[(None,"Select country")] + [(i.country,i.country) for i in Country.objects.all().order_by("country")]
            ),
            "zip": widgets.TextInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "10013"
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

