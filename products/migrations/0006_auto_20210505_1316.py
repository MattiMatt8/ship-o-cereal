# Generated by Django 3.2 on 2021-05-05 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20210504_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='contents',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=600),
        ),
    ]