# Generated by Django 3.2 on 2021-05-06 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20210506_1304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='address',
            new_name='street_name',
        ),
        migrations.AddField(
            model_name='address',
            name='house_number',
            field=models.IntegerField(default=23),
            preserve_default=False,
        ),
    ]
