# Generated by Django 5.1.1 on 2024-10-08 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auctions_min_price'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Auctions',
            new_name='Auction',
        ),
        migrations.RenameModel(
            old_name='Bids',
            new_name='Bid',
        ),
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]
