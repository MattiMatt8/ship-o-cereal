from django.forms import ModelForm
from users.models import SearchHistory


class AddSearchHistoryForm(ModelForm):
    class Meta:
        model = SearchHistory
        fields = ("search",)
