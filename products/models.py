from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Label(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    contents = models.TextField(blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING)
    weight = models.IntegerField(blank=True, null=True)
    stock = models.IntegerField(default=0)
    active = models.BooleanField(default=True, null=True)
    # Total review score before dividing by total of reviewers
    total_review_score = models.FloatField(default=0, blank=True)
    # Total people that have reviewed the product
    total_reviewers = models.IntegerField(default=0, blank=True)
    # Current review calculated already
    review_calculated = models.FloatField(default=0, blank=True)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    percentage_off = models.FloatField(default=0, blank=True)
    discounted_price = models.FloatField(blank=True, null=True)
    labels = models.ManyToManyField(Label, through="ProductLabel")
    reviews = models.ManyToManyField(User, through="Review")

    def __str__(self):
        return self.name

    class Meta:
        indexes = [models.Index(fields=["name"])]


class Image(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class ProductLabel(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    label = models.ForeignKey(Label, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ("product", "label")


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=now)
    stars = models.IntegerField()
    review = models.TextField(max_length=500)
    title = models.CharField(max_length=255)

    class Meta:
        unique_together = ("user", "product")
        ordering = ["-id"]

    def __str__(self):
        return self.review
