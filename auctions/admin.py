from django.contrib import admin

from .models import User, Listings, Bids, Comments, Category

admin.site.register(User)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Category)
admin.site.register(Listings)