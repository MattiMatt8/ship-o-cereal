from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Label(models.Model):
    """All product labels (e.g. Healthy, Glutenfree...)"""
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    """All product categories (e.g. Cereal, Bowls...)"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Brand(models.Model):
    """All product brands."""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Product(models.Model):
    """Product with all its relative information."""
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
        """To make the search faster by having an index on the name field."""
        indexes = [models.Index(fields=["name"])]


def make_filename(instance, filename):
    """Makes the filename for product image uploaded."""
    return "product_images/" + str(instance.product.category) + "/" + filename


class Image(models.Model):
    """Product images, each product can have many images."""
    name = models.ImageField(upload_to=make_filename, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"ID: {self.id}"


class ProductLabel(models.Model):
    """Product labels, each product can have many labels."""
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    label = models.ForeignKey(Label, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ("product", "label")

    def __str__(self):
        return self.label.name


class Review(models.Model):
    """Product reviews made by users."""
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=now)
    stars = models.IntegerField()
    review = models.TextField(max_length=500)
    title = models.CharField(max_length=255)

    class Meta:
        # Unique together so it enforces that each user
        # can only make one review on each product.
        unique_together = ("user", "product")
        ordering = ["-id"]

    def __str__(self):
        return self.review
