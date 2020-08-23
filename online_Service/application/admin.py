from django.contrib import admin
from .models import Goods, Ratings, UserProfile, CreditCards, Ordered


admin.site.register(Goods)
admin.site.register(Ratings)
admin.site.register(UserProfile)
admin.site.register(CreditCards)
admin.site.register(Ordered)