# Generated by Django 3.2 on 2021-05-05 01:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
