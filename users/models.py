from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from products.models import Product


def make_filename(instance, filename):
    return "profile_images/" + str(instance.user.id) + "." + filename.split(".")[-1]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=make_filename, blank=True, null=True)
    phone = models.CharField(max_length=255)


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    holder = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    month = models.IntegerField()
    year = models.IntegerField()

    class Meta:
        ordering = ["id"]


class Country(models.Model):
    country = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.country


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    street_name = models.CharField(max_length=255)
    house_number = models.IntegerField()
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    additional_comments = models.CharField(max_length=255, blank=True, null=True)
    zip = models.IntegerField()
    city = models.CharField(max_length=255)

    class Meta:
        ordering = ["id"]


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=now)
    search = models.CharField(max_length=255)

    class Meta:
        ordering = ["-id"]
