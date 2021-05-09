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
    status = models.CharField(max_length=255) # Maybe smaller?
    shipping_cost = models.FloatField()
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    card = models.ForeignKey(Card, on_delete=models.DO_NOTHING)
    items = models.ManyToManyField(Product, through='OrderItem')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.FloatField()

    class Meta:
        unique_together = ('order', 'product')