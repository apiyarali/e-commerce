from django.forms import ModelForm
from .models import User, Listings, Bids, Comments, Category

class ListingForm(ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'initial_bid', 'category', 'description', 'image_url', 'is_active']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['category']

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['comments']

class BidForm(ModelForm):
    class Meta:
        model = Bids
        fields = ['bid']