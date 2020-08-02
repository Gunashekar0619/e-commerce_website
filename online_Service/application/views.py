import json
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

    @action(detail=False, methods=['GET'])
    def getusers(self,*args,**kwargs):
        print("egt")
        arra = []
        goods = UserProfile.objects.all()
        for good in goods:
            array = {}
            array["profile_id"] = good.id
            array["user_id"] = good.user_id.id
            array["name"] = good.user_id.username
            array["email"] = good.user_id.email
            array["type"] = good.type
            array["address"] = good.address
            array["city"] = good.city
            array["country"] = good.country
            array["phone_no"] = good.phone_no
            array["gender"] = good.gender
            array["sold"] = good.sold
            array["amount_received"] = good.amount_received
            # print(array)
            arra.append(array)
        # seliazers = ProfileSerializers(arra, many=False)
        response = {'message': 'success', 'result': arra}
        return Response(response, status=status.HTTP_200_OK)


    @action(detail=False,methods=['POST'])
    def seller(self, request):
        if 'user_id' and 'sold' and 'amount_received' in request.data:
            user_id=request.data['user_id']
            currentuser = self.queryset.get(user_id=user_id)
            currentuser.sold= request.data['sold']
            currentuser.amount_received= request.data['amount_received']
            currentuser.save()
            serializer = ProfileSerializers(currentuser,many=False)
            response = {'message':'success','result':serializer.data}
            return Response(response,status=status.HTTP_200_OK)
        else:
            return Response({'Message': 'failed'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk=None):
        # user_id = request.data['user_id']
        # print('user_id')
        # user = User.objects.filter(id=user_id)

        try:
            currentuser = self.queryset.get(user_id=pk)
            currentuser.phone_no= request.data['phone_no']
            currentuser.address = request.data['address']
            currentuser.city = request.data['city']
            currentuser.country = request.data['country']
            currentuser.gender = request.data['gender']

            # currentuser.name = user.username
            currentuser.save()
            serializer = ProfileSerializers(currentuser, many=False)
            response = {'message': 'Profile update', 'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'update error'}
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
                    'user_id':userid,
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

    def get(self,*args,**kwargs):
        print("egt")
        arra = []
        goods = GoodsViewSet.objects.all()
        for good in goods:
            array = {}
            array["goods_id"] = good.id
            array["owner"] = good.user_id.id
            array["location"] = good.location
            array["name"] = good.name
            array["type"] = good.type
            array["price"] = good.price
            array["comments"] = good.comments
            array["stock"] = good.stock
            array["no_of_ratings"] = good.no_of_ratings
            array["avg_ratings"] = good.avg_ratings
            # print(array)
            arra.append(array)
        # seliazers = ProfileSerializers(arra, many=False)
        response = {'message': 'success', 'result': arra}
        return Response(response, status=status.HTTP_200_OK)

    # def put(self,request):
    #     if 'id' and 'owner' in request.data:
    #         product = Goods.objects.get(id=id)
    #         product.name = request.data['name']
    #         product.type = request.data['type']
    #         product.stock = request.data['stock']
    #         product.price = request.data['price']
    #         product.save()
    #         serializer= GoodsSerializers(product,many=False)
    #         response = {"message" : "Product details updated", "data": serializer.data}
    #         return Response(response, status=status.HTTP_200_OK)
    #     else:
    #         return Response({"message":"unsuccessful"},status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def usergoods(self, request):
        if 'user_id' in request.data:
            user_id = request.data['user_id']
            print(user_id)
            list = Goods.objects.filter(owner_id=user_id)
            #print(list)
            goods=[]
            for i in list:
                goods.append(i.id)
            print(goods)
            return Response({'goods_id': goods}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'input user_id'},status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def duplicate(self, request):
        #Count = 0
        if 'name' in request.GET:
            name = request.GET.get('name', '')
            #print(name)
            dupes = Goods.objects.filter(name=name)
            a = len(dupes)
            owner = {}
            for i in dupes:
                owner.update({i.id: {'owerid': i.owner.id, 'name': i.owner.username}})
            return Response({'data': owner, 'count': a}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'give input for duplicate data'})

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