# Generated by Django 3.2 on 2021-05-05 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_card_card_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='additional_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]