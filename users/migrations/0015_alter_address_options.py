# Generated by Django 3.2 on 2021-05-10 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0014_alter_address_country"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="address",
            options={"ordering": ["id"]},
        ),
    ]
