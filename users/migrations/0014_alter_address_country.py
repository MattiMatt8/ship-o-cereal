# Generated by Django 3.2 on 2021-05-10 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0013_auto_20210506_1329"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="country",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="users.country"
            ),
        ),
    ]
