# Generated by Django 3.2 on 2021-05-05 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20210505_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='contents',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=1000),
        ),
    ]
