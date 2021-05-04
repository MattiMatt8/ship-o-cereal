from django.shortcuts import render
from users.forms.RegisterForm import RegisterForm

def register(request):
    return render(request, "users/register.html", {
        "form": RegisterForm()
    })

def profile(request):
    ...