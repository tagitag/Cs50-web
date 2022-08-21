from django.contrib import admin
from .models import Followers, User, Posts


# Register your models here.
admin.site.register(Followers)
admin.site.register(User)
admin.site.register(Posts)
