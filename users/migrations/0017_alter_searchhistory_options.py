# Generated by Django 3.2 on 2021-05-10 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_card_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='searchhistory',
            options={'ordering': ['-id']},
        ),
    ]
