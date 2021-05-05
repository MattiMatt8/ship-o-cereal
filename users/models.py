from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from products.models import Product


# class CartItem(models.Model):
#     user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
#     product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
#     quantity = models.IntegerField()
#
#     class Meta:
#         unique_together = ('user', 'product')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255)
    # cart = models.ManyToManyField(Product, through=CartItem)


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    ssn = models.CharField(max_length=255)
    card_num = models.CharField(max_length=255)
    card_type = models.CharField(max_length=255)
    expiration_date = models.DateField()


class ZipCode(models.Model):
    zip = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=255)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    zip = models.ForeignKey(ZipCode, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    additional_comments = models.CharField(max_length=255, blank=True, null=True)


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=now)
    search = models.CharField(max_length=255)