from django.db import models


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
    labels = models.ManyToManyField(Label)

    def __str__(self): # Maybe add more to the return
        return self.name
