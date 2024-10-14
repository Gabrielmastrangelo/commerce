from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name.capitalize()

class Auction(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=500)  # Limit description to 500 characters
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    date_created = models.DateTimeField(auto_now_add=True)
    url_image = models.URLField(max_length=200, blank=True, null=True)
    min_price = models.FloatField(validators=[MinValueValidator(0.0)])
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="auctions")


    def current_price(self):
        bids = Bid.objects.filter(auction=self)
        if len(bids) > 0:
            return max(bids, key=lambda bid: bid.price).price
        else:
            return None

    def get_winner(self):
        max_price = self.current_price()
        winner = self.bids.get(price=max_price).user
        return winner

    def __str__(self):
        return f'Name: {self.name} - Creator: {self.creator}'


class Bid(models.Model):
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Auction: {self.auction.name} - Bid: {self.price} - User: {self.user.username}'

class Comment(models.Model):
    comment = models.TextField(blank=False)  # No character limit
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Auction: {self.auction.name} - Comment: {self.comment}'


class WatchList(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="interested_users")

    def __str__(self):
        return f'Auction: {self.auction.name} - User: {self.user.username}'
