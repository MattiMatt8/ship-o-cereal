# Generated by Django 3.2 on 2021-05-10 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0006_auto_20210510_0046"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="user",
        ),
    ]