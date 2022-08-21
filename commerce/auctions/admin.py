from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, comments, listings, watchList, bids

admin.site.register(User)
admin.site.register(comments)
admin.site.register(listings)
admin.site.register(watchList)
admin.site.register(bids)
