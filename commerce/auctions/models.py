from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class listings(models.Model):
    # id INTEGER NOT NULL PRINAMRY KEY AUTOINDENT
    id = models.IntegerField(primary_key=True)
    # title TEXT NOT NULL
    title = models.CharField(max_length=100)
    # description TEXT
    description = models.TextField()
    # statring_bid INTEGER NOT NULL
    starting_bid = models.IntegerField()
    # current_bid INTERGER NOT NULL
    current_bid = models.IntegerField(default=-10)
    current_holder = models.IntegerField(default=10)
    # img_url TEXT NOT NULL
    imag_url = models.URLField()
    # catagory TEXT NOT NULL
    catagory = models.TextField()
    # user_id INTEGER NOT NULL
    user_id = models.IntegerField()
    # sold BOOLEAN default false
    sold = models.BooleanField(default=False)
    # sold_for INTEGER NOT NULL default -10
    sold_for = models.IntegerField(default=-10)
    # the id of the user this item was sold to
    sold_to = models.IntegerField(default=-10)

    def __str__(self):
        return f"id: {self.id}, title: {self.title}, description: {self.description}, starting Bid: {self.starting_bid}, current Bid {self.current_bid}, catagory: {self.catagory}, user: {self.user_id} sold: {self.sold}, sold_for: {self.sold_for}"


class bids(models.Model):
    # user_id INTEGER NOT NULL
    user_id = models.IntegerField()
    # amount INTEGER NOT NULL
    amount = models.IntegerField()
    # listing_id INTEGER NOT NULL
    listing_id = models.IntegerField()

    def __str__(self):
        return f"user: {self.user_id}, amount: {self.amount}, listing: {self.listing_id}"


class comments(models.Model):
    # id INTEGER NOT NULL AUTOINDENT PRINAMRY KEY
    id = models.IntegerField(primary_key=True)
    # text TEXT NOT NULL
    text = models.TextField()
    # user_id INTEGER NOT NULL
    user_id = models.IntegerField()
    # listing_id TEXT NOT NULL
    listing_id = models.TextField()
    user_name = models.CharField(max_length=100, default="Anonymus")


class watchList(models.Model):
    user_id = models.IntegerField()
    listing_id = models.IntegerField()
