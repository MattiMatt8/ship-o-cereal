# Generated by Django 3.2 on 2021-05-11 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Status',
        ),
    ]
