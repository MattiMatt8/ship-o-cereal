# Generated by Django 3.2 on 2021-05-09 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_auto_20210509_0133"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(default="Placed", max_length=255),
        ),
    ]
