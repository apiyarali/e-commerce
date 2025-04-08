from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from decimal import Decimal


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listings', blank="True", related_name="users")

    class Meta:
        verbose_name_plural="Users"

    def __str__(self):
        return f"{self.id}: {self.username}"

class Listings(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=255)
    initial_bid = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="listings")
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name_plural="Listings"

    def __str__(self):
        return f"""
                {self.id}: {self.title},
                Posted by: {self.seller.username},
                Price: {self.initial_bid},
                Category: {self.category},
                Description: {self.description},
                Created: {self.created},
                """

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=6, decimal_places=2, blank=True, default=0.00)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")
    created = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name_plural="Bids"

    def __str__(self):
        return f"""
                {self.id}: {self.user.username}, 
                bids on {self.listing.title},
                for {self.bid}
                """

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments")
    comments = models.TextField(blank=True)
    created = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name_plural="Comments"

    def __str__(self):
        return f"""
                {self.id}: {self.user.username}, 
                Commented: {self.comments},
                For listing: {self.listing.title},
                On: {self.created}.
                """
    
class Category(models.Model):
    category = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural="Category"

    def __str__(self):
        return f"{self.category}"