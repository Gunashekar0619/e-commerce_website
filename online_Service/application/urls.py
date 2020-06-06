from .views import GoodsViewSet, RatingsViewSet, UserViewSet, ProfileViewSet, CustomAuthToken, Userdetails
from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from rest_framework.authtoken.views import obtain_auth_token


router = routers.DefaultRouter()
router.register('Goods',GoodsViewSet)
router.register('Ratings',RatingsViewSet)
router.register('user',UserViewSet)
router.register('profile',ProfileViewSet)
#router.register('userdetails',Userdetails)



urlpatterns = [
    path('',include(router.urls)),
    path('auth/',CustomAuthToken.as_view()),
    path('userdetails/',Userdetails.as_view())
]