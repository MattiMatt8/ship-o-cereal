# Generated by Django 3.2 on 2021-05-05 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='card_type',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
