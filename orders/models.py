from django.db import models
from products.models import Product
from django.utils.timezone import now
from django.contrib.auth.models import User
from users.models import Address, Card


class Status(models.Model):
    """Model for the status of an order."""

    name = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Order(models.Model):
    """Model for users purchase order."""

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    total = models.FloatField()
    products_total = models.FloatField()
    date = models.DateTimeField(default=now)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
    shipping_cost = models.FloatField()
    items = models.ManyToManyField(Product, through="OrderItem")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    address_street_name = models.CharField(max_length=255)
    address_house_number = models.CharField(max_length=255)
    address_city = models.CharField(max_length=255)
    address_zip = models.IntegerField()
    address_country = models.CharField(max_length=255)
    address_additional_comments = models.CharField(
        max_length=255, blank=True, null=True
    )

    @property
    def order_items(self):
        return self.orderitem_set.all()

    def __str__(self):
        return f"Order number: {self.id}"

    class Meta:
        ordering = ["-id"]


class OrderItem(models.Model):
    """Model for each product a user buys and it connects to the order model."""

    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.FloatField()

    class Meta:
        unique_together = ("order", "product")
