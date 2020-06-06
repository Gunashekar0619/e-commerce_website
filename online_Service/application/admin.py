from django.contrib import admin
from .models import Goods, Ratings, UserProfile


admin.site.register(Goods)
admin.site.register(Ratings)
admin.site.register(UserProfile)