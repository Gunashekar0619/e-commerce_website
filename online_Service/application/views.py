from rest_framework.views import APIView
from .models import Goods, Ratings, UserProfile
from .serializers import UserSerializers, GoodsSerializers, RatingsSerializers, ProfileSerializers
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
#from django.contrib.auth import get_user_model
#user1=get_user_model()


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk=None):
        try:
            currentuser = self.queryset.get(user_id=pk)
            currentuser.phone_no= request.data['phone_no']
            currentuser.address = request.data['address']
            currentuser.city = request.data['city']
            currentuser.country = request.data['country']
            currentuser.gender = request.data['gender']
            currentuser.save()
            serializer = ProfileSerializers(currentuser, many=False)
            response = {'message': 'Profile update', 'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'failed'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    @action(detail=True, methods=['POST'])
    def update12(self, request, pk=None):
        try:
            currentuser = self.queryset.get(id=pk)
            #password = request.data['password']
            currentuser.username = request.data['username']
            currentuser.email = request.data['email']
            #currentuser.set_password('password')
            currentuser.save()
            serializer = UserSerializers(currentuser, many=False)
            response = {'message': 'Profile update', 'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'failed'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class Userdetails(APIView):

   # @action(detail=True, methods=['get'])
    def post(self, request):
        if 'user_id' in request.data:
            userid = request.data['user_id']
            try:
                user = UserProfile.objects.get(user_id=userid)
                response = {'status': ' fetch success', 'data': {
                    'profile_id': user.id,
                    'phone_no': user.phone_no,
                    'type': user.type,
                    'address': user.address,
                    'city': user.city,
                    'country':user.country,
                    'gender':user.gender
                }}
                return Response(response, status=status.HTTP_200_OK)
            except:
                response = {'status': 'failure', 'message': 'enter valid user id'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'enter user_id'}, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data,
                                               context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': 'success', 'data': {
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'email': user.email
            }}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'failure', 'result': 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class GoodsViewSet(viewsets.ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['POST'])
    def rate_goods(self, request, pk=None):
        if 'stars' in request.data:
            goods = Goods.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            try:
                rating = Ratings.objects.get(user=user.id, good=goods.id)
                rating.stars = stars
                rating.save()
                serializer = RatingsSerializers(rating, many=False)
                response = {'message': 'ratings update', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

            except:
                rating = Ratings.objects.create(user=user, good=goods, stars=stars)
                serializer = RatingsSerializers(rating, many=False)
                response = {'message': 'Rating Created', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': 'its not working'}
            return Response(response, status.HTTP_200_OK)


class RatingsViewSet(viewsets.ModelViewSet):
    queryset = Ratings.objects.all()
    serializer_class = RatingsSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        response = {'message': 'Rating cannot be modify like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'Rating cannot be created like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)