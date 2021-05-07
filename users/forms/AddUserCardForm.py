from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.forms import widgets, ModelForm
from django.utils.timezone import now
from users.models import Card


class AddUserCardForm(ModelForm):
    class Meta:
        FIELD_STYLE = "border border-customGray rounded px-4 shadow-inner w-full h-8 placeholder-gray-300 focus:outline-none"
        model = Card
        fields = ("holder", "number", "month", "year")
        widgets = {
            "holder": widgets.TextInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "Bob Ross"
                }
            ),
            "number": widgets.TextInput(
                attrs={
                    "class": FIELD_STYLE,
                    "placeholder": "1111-2222-3333-4444"
                }
            ),
            "month": widgets.Select(
                attrs={
                    "class": "border border-customGray rounded px-4 shadow-inner w-24 h-8 placeholder-gray-300 focus:outline-none",
                    "required": True
                },
                choices=[(None, "Month")] + [(num, num) for num in range(1, 13)]
            ),
            "year": widgets.Select(
                attrs={
                    "class": "border border-customGray rounded px-4 shadow-inner ml-2 w-28 h-8 placeholder-gray-300 focus:outline-none"
                },
                choices=[(None, "Year")] + [(num, num) for num in range(now().year, now().year + 21)]
            )
        }

    def checkCardNumField(self, card_field):
        if len(card_field) != 4 or not card_field.isnumeric():
            return False
        return True

    def checkCardNum(self, card_num):
        card = card_num.split("-")
        if len(card) != 4:
            return False
        for card_field in card:
            if not self.checkCardNumField(card_field):
                return False
        return True

    def clean_number(self):
        number = self.cleaned_data["number"]
        if not self.checkCardNum(number):
            raise ValidationError([
                ValidationError(_('Invalid card number.')),
                ValidationError(_('Required 16 digits, no letters.')),
            ])
        return number
