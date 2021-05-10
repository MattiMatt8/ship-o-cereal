from django.db import models
from products.models import Product
from django.utils.timezone import now
from django.contrib.auth.models import User

from users.models import Address, Card


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    total = models.FloatField()
    products_total = models.FloatField()
    date = models.DateTimeField(default=now)
    status = models.CharField(max_length=255, default="Placed") # Maybe smaller?
    shipping_cost = models.FloatField()
    items = models.ManyToManyField(Product, through='OrderItem')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    address_street_name = models.CharField(max_length=255)
    address_house_number = models.CharField(max_length=255)
    address_city = models.CharField(max_length=255)
    address_zip = models.IntegerField()
    address_country = models.CharField(max_length=255)
    address_additional_comments = models.CharField(max_length=255)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.FloatField()

    class Meta:
        unique_together = ('order', 'product')