from django.core.exceptions import ValidationError
from django.forms import widgets, ModelForm
from products.models import Review


class AddReview(ModelForm):

    def clean_stars(self):
        stars = self.cleaned_data["stars"]
        if stars < 1 or stars > 5:
            raise ValidationError("Invalid amount of stars.")
        return self.cleaned_data["stars"]

    class Meta:
        model = Review
        fields = ("stars", "review")
        widgets = {
            "stars": widgets.NumberInput(
                attrs={
                    "class": "hidden"
                }
            ),
            "review": widgets.Textarea(
                attrs={
                    "class": "border border-customGray rounded py-4 px-4 shadow-inner w-full placeholder-gray-300 focus:outline-none",
                    "placeholder": "I thought it was..."
                }
            )
        }