from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Label(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    contents = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True) # Blank?
    weight = models.IntegerField(blank=True)
    stock = models.IntegerField(default=0)
    active = models.BooleanField(default=True) # Default?
    total_score = models.FloatField(default=0) # Need to check, review should update this each time
    total_reviews = models.IntegerField(default=0) # Need to check, review should update this each time
    price = models.FloatField()
    category = models.CharField(max_length=255)
    percentage_off = models.FloatField(default=0)
    picture = models.CharField(max_length=255)
    labels = models.ManyToManyField(Label, through='ProductLabel')
    reviews = models.ManyToManyField(User, through='Review')

    def __str__(self): # Maybe add more to the return
        return self.name


class ProductLabel(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    label = models.ForeignKey(Label, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('product', 'label')


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=now)
    stars = models.FloatField()
    review = models.CharField(max_length=255)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self): # todo: Add more to the return
        return self.review
