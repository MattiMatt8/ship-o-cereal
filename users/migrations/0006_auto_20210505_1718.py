# Generated by Django 3.2 on 2021-05-05 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_address_additional_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='zip',
            field=models.IntegerField(),
        ),
        migrations.DeleteModel(
            name='ZipCode',
        ),
    ]