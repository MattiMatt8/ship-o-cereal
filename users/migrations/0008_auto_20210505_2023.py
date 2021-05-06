# Generated by Django 3.2 on 2021-05-05 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210505_2017'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='name',
            new_name='holder',
        ),
        migrations.RemoveField(
            model_name='card',
            name='expiration_date',
        ),
        migrations.AddField(
            model_name='card',
            name='month',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='card',
            name='year',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]