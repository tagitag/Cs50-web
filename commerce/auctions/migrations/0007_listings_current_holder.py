# Generated by Django 4.1 on 2022-08-14 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_listings_sold_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='current_holder',
            field=models.IntegerField(default=10),
        ),
    ]
