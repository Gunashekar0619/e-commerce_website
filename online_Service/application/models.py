from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import date, datetime


class UserProfile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, blank=False)
    phone_no = models.IntegerField()
    address = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=100,blank=True)
    country = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    gender = models.CharField (max_length=10,blank=True)
    sold = models.IntegerField(default=0)
    amount_received = models.IntegerField(default=0)
    pincode = models.IntegerField(default=0)


class Goods(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE, null= True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20)
    price = models.IntegerField()
    comments = models.CharField(max_length=100, blank=True)
    stock = models.IntegerField()
    location = models.CharField(max_length=200,default="")
    pincode = models.IntegerField(default=0)

    def no_of_ratings(self):
        rating = Ratings.objects.filter(good=self)
        l = len(rating)
        return l

    def avg_ratings(self):
        sum = 0
        rating = Ratings.objects.filter(good=self)
        l = len(rating)
        for rating in rating:
            sum += rating.stars
        if l > 0:
            return sum / l
        else:
            return 0


class Ratings(models.Model):
    good = models.ForeignKey(Goods, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = (('user', 'good'),)
        index_together = (('user', 'good'),)


class CreditCards(models.Model):
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)
    cardNumber = models.IntegerField()
    cardName = models.CharField(max_length=100)
    expiry = models.IntegerField()
    cvc = models.IntegerField()


class Ordered(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cardNumber = models.IntegerField()
    date = models.DateField(default=date.today)
    time = models.TimeField(default=datetime.now().strftime("%H:%M:%S"))
    Goods = models.CharField(max_length=100)
    price = models.IntegerField()
    shipmentAddress = models.CharField(max_length=500)
    phone_no = models.IntegerField(default=0)
    sellerId = models.IntegerField(default=0)
    seller = models.CharField(max_length=100)
    transationid = models.IntegerField()
    success = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)
    total = models.IntegerField(default=0)