# Generated by Django 3.2 on 2021-05-05 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20210505_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='contents',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(),
        ),
    ]