# Generated by Django 3.2 on 2021-05-11 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_order_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
