# Generated by Django 4.1 on 2022-08-15 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_watchlist_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='user_name',
        ),
        migrations.AddField(
            model_name='comments',
            name='user_name',
            field=models.CharField(default='Anonymus', max_length=100),
        ),
    ]
