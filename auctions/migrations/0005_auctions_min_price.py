# Generated by Django 5.1.1 on 2024-09-16 13:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_remove_auctions_image_auctions_url_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctions',
            name='min_price',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0)]),
            preserve_default=False,
        ),
    ]
