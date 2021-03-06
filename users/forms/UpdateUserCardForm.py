from django.forms import widgets, ModelForm
from django.utils.timezone import now
from users.models import Card


class UpdateUserCardForm(ModelForm):
    class Meta:
        FIELD_STYLE = "border border-customGray rounded px-4 shadow-inner w-full h-8 placeholder-gray-300 focus:outline-none"
        model = Card
        fields = ("holder", "month", "year")
        widgets = {
            "holder": widgets.TextInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "Bob Ross"
                }
            ),
            "month": widgets.Select(
                attrs={
                    "class": "border border-customGray rounded px-4 shadow-inner w-26 h-8 placeholder-gray-300 focus:outline-none",
                    "placeholder": "2012",
                    "required": True
                },
                choices=[(None,"Month")] + [(num,num) for num in range(1,13)]
            ),
            "year": widgets.Select(
                attrs={
                    "class": "border border-customGray rounded px-4 shadow-inner ml-2 w-28 h-8 placeholder-gray-300 focus:outline-none",
                    "placeholder": "2012"
                },
                choices=[(None,"Year")] + [(num,num) for num in range(now().year,now().year+21)]
            )
        }
