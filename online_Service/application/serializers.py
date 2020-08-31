from rest_framework import serializers
from .models import Goods, Ratings, UserProfile, CreditCards, Ordered
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class ProfileSerializers(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {'type': {'required': True},
                        'phone_no': {'required': True},
                        'pincode':{'required':True}
                        }


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class GoodsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ('id','owner', 'name', 'type', 'price', 'comments', 'stock','location','pincode', 'no_of_ratings', 'avg_ratings')
        extra_kwargs = {'name': {'required': True},
                        'type': {'required': True},
                        'price': {'required': True},
                        'stock': {'required': True}
                        }


class RatingsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = ('id', 'stars', 'user', 'good')
        extra_kwargs = {'stars': {'required': True}}


class CreditSerializers(serializers.ModelSerializer):
    class Meta:
        model = CreditCards
        fields = '__all__'
        extra_kwargs = {'Owner': {'required': True},
                        'cardNumber': {'required': True},
                        }


class OrderedSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ordered
        fields = '__all__'
        extra_kwargs = {'user': {'required': True},
                        'cardNumber': {'required': True},
                        'Goods': {'required': True},
                        'seller': {'required': True}
                        }