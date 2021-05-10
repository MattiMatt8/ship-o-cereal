from django.forms import widgets, ModelForm
from products.models import Review


class AddUserCardForm(ModelForm):
    class Meta:
        FIELD_STYLE = "border border-customGray rounded px-4 shadow-inner w-full h-8 placeholder-gray-300 focus:outline-none"
        model = Review
        fields = ("stars", "review")
        widgets = {
            "stars": widgets.NumberInput( # TODO: Hmmm
                attrs={
                    "class": FIELD_STYLE
                }
            ),
            "review": widgets.TextInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "I thought it was..."
                }
            )
        }