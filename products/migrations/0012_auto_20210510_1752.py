# Generated by Django 3.2 on 2021-05-10 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_product_products_pr_name_9ff0a3_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discounted_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='percentage_off',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
