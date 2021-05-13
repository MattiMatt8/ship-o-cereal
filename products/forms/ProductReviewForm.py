from django.core.exceptions import ValidationError
from django.forms import widgets, ModelForm
from products.models import Review


class ProductReviewForm(ModelForm):

    def clean_stars(self):
        """Makes it so that the stars given can only be in the range of 1-5."""
        stars = self.cleaned_data["stars"]
        if stars < 1 or stars > 5:
            raise ValidationError("Invalid amount of stars.")
        return self.cleaned_data["stars"]

    class Meta:
        """Defining how the form will be and look."""
        model = Review
        fields = ("stars", "review", "title")
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
            ),
            "title": widgets.TextInput(
                attrs={"class": "border border-customGray rounded px-4 shadow-inner w-full h-8 placeholder-gray-300 focus:outline-none"}
            ),
        }