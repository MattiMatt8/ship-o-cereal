from django.forms import ModelForm
from users.models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ("phone", "picture")